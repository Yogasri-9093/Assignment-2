import random

# Define vocab groups (topics)
BIG_DATA = ["hadoop", "mapreduce", "spark", "data", "analytics", "cloud",
            "distributed", "parallel", "processing", "cluster"]

ML = ["machine", "learning", "neural", "model", "training", "testing",
      "inference", "natural", "language", "processing"]

DATABASE = ["database", "query", "storage", "system", "performance",
            "scalability", "network", "security", "index"]

COMMON = ["python", "java", "algorithm", "big", "mining", "stream", "tokenization", 
          "stemming", "similarity", "document"]

def generate_biased_doc(doc_name, length, main_topic, bias=0.7):
    """Generate a document with topic bias."""
    doc_words = []
    for _ in range(length):
        if random.random() < bias:  # Pick from main topic
            doc_words.append(random.choice(main_topic))
        else:  # Pick from other/common words
            pool = BIG_DATA + ML + DATABASE + COMMON
            doc_words.append(random.choice(pool))
    return f"{doc_name} " + " ".join(doc_words) + "\n"

def generate_dataset(filename):
    with open(filename, "w") as f:
        f.write(generate_biased_doc("Document1", 1000, BIG_DATA))
        f.write(generate_biased_doc("Document2", 3000, ML))
        f.write(generate_biased_doc("Document3", 5000, DATABASE))
    print(f"{filename} generated with topic-biased documents.")

if __name__ == "__main__":
    generate_dataset("documentdataset.txt")
