# Assignment 2: Document Similarity using MapReduce

**Name:** Yogasri Lella

**Student ID:** 801428972

## Approach and Implementation

### Mapper Design
The Mapper reads each document from HDFS line by line.

**Input key-value pair:**

Key: The document ID (Text)

Value: The content of the document (Text)

**Logic:**

Tokenizes the document into words.

Emits the document ID as the key and a comma-separated list of words as the value.

**Output key-value pair:**

Key: Document ID (Text)

Value: Comma-separated list of words in the document (Text)

**Purpose:**

Prepares the data for the Reducer to compute pairwise document similarities efficiently.
### Reducer Design
The Reducer receives all documents’ word lists.

**Input key-value pair:**

Key: Document ID (Text)

Value: List of words in the document (Text)

**Logic:**

Stores all documents’ IDs and word sets.

For each unique pair of documents, calculates Jaccard Similarity:

J(A,B)=∣A∪B∣/∣A∩B∣
	​
Emits only pairs with similarity ≥ 50%.

**Output key-value pair:**

Key: Pair of document IDs (Text)

Value: Similarity percentage (Text)

**Purpose:**

Computes pairwise similarities between documents and filters out low-similarity pairs.

### Overall Data Flow
**1. Input:** HDFS stores the documents as text files.

**2. Mapper Phase:** Each document is tokenized into a set of words, producing (docID, wordList) pairs.

**3. Shuffle and Sort Phase:** Hadoop groups the output of the Mapper by key (document ID).

**4. Reducer Phase:**

-Collects all document word sets.

-Computes Jaccard Similarity for each document pair.

-Outputs only the pairs with similarity ≥ 50%.

**5. Output:** HDFS stores the final results as (doc1, doc2) → similarity%.

---

## Setup and Execution

### 1. **Start the Hadoop Cluster**

Run the following command to start the Hadoop cluster:

```bash
docker compose up -d
```

### 2. **Build the Code**

Build the code using Maven:

```bash
mvn clean package
```

### 3. **Move JAR File to Shared Folder**

Move the generated JAR file to a shared folder for easy access:

```bash
mv target/*.jar shared-folder/input/
```

### 4. **Copy JAR to Docker Container**

Copy the JAR file to the Hadoop ResourceManager container:

```bash
docker cp shared-folder/input/DocumentSimilarity-0.0.1-SNAPSHOT.jar resourcemanager:/opt/hadoop-3.2.1/share/hadoop/mapreduce/
```

### 5. **Move Dataset to Docker Container**

Copy the dataset to the Hadoop ResourceManager container:

```bash
docker cp shared-folder/input/docdataset1.txt resourcemanager:/opt/hadoop-3.2.1/share/hadoop/mapreduce/
```

### 6. **Connect to Docker Container**

Access the Hadoop ResourceManager container:

```bash
docker exec -it resourcemanager /bin/bash
```

Navigate to the Hadoop directory:

```bash
cd /opt/hadoop-3.2.1/share/hadoop/mapreduce/
```

### 7. **Set Up HDFS**

Create a folder in HDFS for the input dataset:

```bash
hadoop fs -mkdir -p /input/dataset
```

Copy the input dataset to the HDFS folder:

```bash
hadoop fs -put ./docdataset1.txt /input/dataset
```

### 8. **Execute the MapReduce Job**

Run your MapReduce job using the following command: Here I got an error saying output already exists so I changed it to output1 instead as destination folder

```bash
hadoop jar /opt/hadoop-3.2.1/share/hadoop/mapreduce/DocumentSimilarity-0.0.1-SNAPSHOT.jar com.example.DocumentSimilarityDriver /input/dataset/docdataset1.txt /1node_output1
```

### 9. **View the Output**

To view the output of your MapReduce job, use:

```bash
hadoop fs -cat /1node_output1/*
```

### 10. **Copy Output from HDFS to Local OS**

To copy the output from HDFS to your local machine:

1. Use the following command to copy from HDFS:
    ```bash
    hdfs dfs -get /node1_output1 /opt/hadoop-3.2.1/share/hadoop/mapreduce/
    ```

2. use Docker to copy from the container to your local machine:
   ```bash
   exit 
   ```
    ```bash
    docker cp resourcemanager:/opt/hadoop-3.2.1/share/hadoop/mapreduce/node1_output1/ shared-folder/output/
    ```
3. Commit and push to your repo so that we can able to see your output


---

## Challenges and Solutions

**Challenge 1: Managing different Hadoop nodes (1-node vs 3-node cluster)**

-Problem: Execution times varied significantly between single-node and multi-node setups.

-Solution: Observed job counters and timings to understand resource utilization; documented the difference in execution time in the README.

**Challenge 2: Handling large input files and word tokenization**

-Problem: Large datasets could cause memory issues or incorrect tokenization.

-Solution: Split documents into words carefully, removed extra spaces, and tested with increasing dataset sizes to ensure consistency.

---
## Sample Input

**Input from `small_dataset.txt`**
```
Document1 This is a sample document containing words
Document2 Another document that also has words
Document3 Sample text with different words
```
## Sample Output

**Output from `small_dataset.txt`**
```
"Document1, Document2 Similarity: 0.56"
"Document1, Document3 Similarity: 0.42"
"Document2, Document3 Similarity: 0.50"
```
## Obtained Output: 
```
(Document1, Document2)	11%

(Document1, Document3)	17%

(Document2, Document3)	8%
```
## Execution time Observation:
**3 Nodes:**

Total map time across all slots: 6440 ms

Total reduce time across all slots: 13288 ms

CPU time spent: 690 ms

Job completed in roughly 13 seconds (from submission to completion).

**1 Node:**

Total map time across all slots: 6696 ms

Total reduce time across all slots: 13472 ms

CPU time spent: 700 ms

Job completed in roughly 14 seconds.

---
## Conclusion

-The MapReduce program successfully computes the Jaccard Similarity between documents in a distributed environment using Hadoop.

-Using Mapper and Reducer, the solution efficiently tokenizes documents, generates unique document pairs, and calculates similarity scores.

-The program demonstrates the scalability of Hadoop, handling datasets across single-node and multi-node clusters, with noticeable differences in execution time.

-Overall, this assignment highlights the effectiveness of distributed processing for large-scale document similarity analysis.

