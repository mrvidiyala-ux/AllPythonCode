from gpt4all import GPT4All

model = GPT4All(
    model_name="Llama-3.2-3B-Instruct-Q4_0.gguf",
    model_path=r"C:\Users\SaiJashwanth\AppData\Local\nomic.ai\GPT4All",
    device="cpu"
)

with model.chat_session():
    while True:
        user = input("You: ")
        if user.lower() in ["exit", "quit"]:
            break
        response = model.generate(
            user,
            max_tokens=200,
            temp=0.7
        )
        print("AI:", response)
