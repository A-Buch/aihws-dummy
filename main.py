# %%
import os
import time
from glob import glob
from pathlib import Path
from io import StringIO

import pandas as pd
from jinja2 import Environment, FileSystemLoader
from langchain_docling import DoclingLoader
import transformers
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    BitsAndBytesConfig,
)
import torch
import gc  # cleaning up

from settings import settings as s



def main(text_sources: list):
    

    start_time = time.time()

    ## Lets check how many documents we will use for extracting information about hazard impacts on infrastructure
    print(f"Number of text sources to process: {len(text_sources)}")

    # ## LLM v1 (first attempt )
    device = transformers.infer_device()
    print(f"Using device: {device}")

    # Name the model and tokenizer we want to use for text mining
    model_name = "meta-llama/Llama-2-7b-chat-hf"
    print(f"Using model: {model_name}")

    # ### Prompt 1
    # The step comprises some prompt engineering by loading a prompt template with some prompt variables: user "question" and "context". The latter refers to the text chunks that are passed to the model iteratively while scanning through each document, the former to the question of the user (defined in the code block below)

    # %%
    question = "Which infrastructure failures are mentioned in the text? Categorize the output by the type of infrastructure, the location, and the type of damage."

    # %%
    env = Environment(loader=FileSystemLoader("./prompt_templates/"))
    prompt_template = env.get_template("simple_prompt.txt")

    # quantization
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_use_double_quant=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.float16,
    )

    ## check that cuda is ready
    torch.cuda.empty_cache()
    print(torch.cuda.memory_reserved() / 1e9)

    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        dtype="auto",
        # attn_implementation="flash_attention_2",
        quantization_config=bnb_config,
        local_files_only=True,  # <-- uncomment when already downloaded model once
    )
    # model.save_pretrained("./huggingface_mirror/hub/")

    tokenizer = AutoTokenizer.from_pretrained(
        model_name,
        use_fast=True,
        local_files_only=True,  # <-- uncomment when already downloaded model once
    )
    # tokenizer.save_pretrained("./huggingface_mirror/hub/")

    # For the people with GPU:
    # It might also be benefical to reduce memory usage furhter by moving the model to the GPU and enabling checkpointing. However the latter is only benefical when you want to do model training, however, for now we just use the (pre-trained) LLM for inference (ie. prediction)
    model = model.to(device)
    model.use_checkpointing = (
        True  # <<-- uncomment when you want to reduce GPU memory usage during training
    )

    ###  ------------ Run the text mining pipeline  ---------------

    df_responses_all = pd.DataFrame()

    ## initialize pipeline
    pipeline = transformers.pipeline(  # load model locally from .cache\
        task="text-generation",
        model=model,
        tokenizer=tokenizer,
        device_map="auto",
    )

    for i, filename in enumerate(text_sources):
        no_documents = len(text_sources)
        filepath = Path(filename)

        ## load document and break into chunks
        loader = DoclingLoader(filepath)
        doc = loader.load()

        print(
            f"\n\n ######## -------- Processing document [{i + 1}/{no_documents}]: {filepath.name} -------- ######## \n"
        )

        for j, chunk in enumerate(doc):
            print("chunk:", j)

            ## render prompt
            context = [{"text": chunk.page_content}]

            rendered_prompt = prompt_template.render(
                context=context,
                question=question,
            )

            # call pipeline on the respective chunk
            response = pipeline(
                text_inputs=rendered_prompt,
                max_new_tokens=1024,
                do_sample=True,
                num_beams=1,
                temperature=0.2,
                eos_token_id=tokenizer.eos_token_id,
                return_full_text=False,
            )
            # postprocess response
            resp = response[0]["generated_text"].replace("\n", "")
            try:
                resp = pd.read_json(StringIO(resp))
                resp["filename"] = filepath.name
                resp["chunk"] = chunk.page_content
                df_responses_all = pd.concat(
                    [df_responses_all, resp], ignore_index=True
                )
            except ValueError as e:
                print(f"Cannot add response to output dataframe: {e}, \n{resp}")
                pass

        # empty CUDA cache for next document
        gc.collect()
        torch.cuda.empty_cache()

    # Save the final LLm output to .csv for later usage with some downstream models
    if not os.path.isfile(PATH_LLM_DATA):
        print(
            f"Saving prompt and LLM response [.txt, .csv] to {LLM_OUTPUT_FILEPATH} ..."
        )

        with open(f"prompt_{PATH_LLM_DATA.stem}.txt", "w") as f:
            f.write(prompt_template.render(context=context, question=question))
        df_responses_all.to_csv(LLM_OUTPUT_FILEPATH, index=False)

    else:
        print(
            f"Output file {Path(LLM_OUTPUT_FILEPATH).stem} already exists. Skip saving to avoid overwriting ..."
        )

    print(f"Text mining of documents done, postprocessed LLM output is saved to {LLM_OUTPUT_FILEPATH}.")
    print(f"Time elapsed: {(time.time() - start_time) / 60:.2f} minutes.")


if __name__ == "__main__":

    # load data paths
    
    DATA_DIR = s.PATH_DATA
    PATH_LLM_DATA = s.PATH_LLM_DATA
    LLM_OUTPUT_FILEPATH = PATH_LLM_DATA / s.LLM_DATA_FILENAME

    ## load dtaa to process
    ## NOTE: we limit the data extraction to only two publications at the moment to exemplify how the LLM application works
    text_sources = glob(str(Path(DATA_DIR, "*_cleaned.md")))[:2]

    ## run text mining pipeline
    main(text_sources)
