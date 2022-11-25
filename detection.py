import torch
import transformers

model: transformers.GPT2LMHeadModel = transformers.GPT2LMHeadModel.from_pretrained("gpt2")
tokenizer = transformers.GPT2Tokenizer.from_pretrained("gpt2")

# model: transformers.T5ForConditionalGeneration = transformers.T5ForConditionalGeneration.from_pretrained("t5-base")
# tokenizer = transformers.T5Tokenizer.from_pretrained("t5-base")
# print(tokenizer.get_vocab())

def find_neighbors(word, k=20):
    tokens = tokenizer.encode(word, add_special_tokens=False)
    output_embeddings = model.lm_head.weight
    dot_similarity = torch.einsum("n,vn->v", output_embeddings[tokens[0]], output_embeddings)
    max_values, max_indices = torch.topk(dot_similarity, k=k)
    print("Word:", word)
    print(tokenizer.tokenize(word))
    for i, (index, value) in enumerate(zip(max_indices, max_values)):
        print(f"Rank {i + 1} | ({tokenizer.convert_ids_to_tokens(index.item())}, {value.item()})")

find_neighbors("2")
find_neighbors("two")
find_neighbors("director")
find_neighbors("woman")
find_neighbors("basketball")
