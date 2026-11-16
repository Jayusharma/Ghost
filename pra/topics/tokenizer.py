from transformers import AutoTokenizer

sentence = "hello world"

tokenizer = AutoTokenizer.from_pretrained("bert-base-cased")

token_ids = tokenizer(sentence)
print(tokenizer.tokenize(sentence))
print(tokenizer.tokenize("unbelievably tokenized"))
print(tokenizer("unbelievably tokenized"))
print(token_ids)

for i in token_ids.input_ids:
    print(tokenizer.decode(i))