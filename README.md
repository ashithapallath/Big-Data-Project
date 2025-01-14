
# Big Data Project  

This repository contains the code and documentation for a Big Data project, focusing on analyzing, processing, and visualizing large-scale datasets. The project includes an implementation of video processing using Kafka for handling real-time data streams.  



## Features  

The project includes:  
- **Data Collection**: Gathering structured and unstructured data from various sources.  
- **Data Preprocessing**: Cleaning, transforming, and preparing datasets for analysis.  
- **Big Data Frameworks**: Utilizing tools like Hadoop, Spark, and Kafka.  
- **Video Processing with Kafka**: Implementing real-time video processing pipelines to handle large video streams.  
- **Analysis and Insights**: Performing advanced analytics using scalable algorithms.  
- **Visualization**: Creating intuitive visualizations to represent trends and findings.  



## Prerequisites  

To run the project, ensure you have the following installed:  
- Python 3.8+  
- Big Data tools such as Hadoop, Apache Spark, and Apache Kafka.  
- Python libraries:  
  - Pandas  
  - PySpark  
  - Matplotlib/Seaborn  
  - Kafka-python  

Install dependencies using pip:  
```bash  
pip install pandas pyspark matplotlib seaborn kafka-python  
```  

 

## How to Use  

1. Clone the repository:  
   ```bash  
   git clone https://github.com/ashithapallath/Big-Data-Project.git  
   cd Big-Data-Project  
   ```  

2. Set up your environment:  
   - Configure Hadoop, Spark, and Kafka on your system (refer to their official documentation).  
   - Ensure your datasets and video files are stored in the appropriate input directories.  

3. Run the Kafka server and create a topic for video processing:  
   ```bash  
   kafka-server-start.sh config/server.properties  
   kafka-topics.sh --create --topic video-stream --bootstrap-server localhost:9092  
   ```  

4. Run the producer to stream video data:  
   ```bash  
   python src/producer.py  
   ```  

5. Run the consumer to process the streamed video data:  
   ```bash  
   python src/consumer.py  
   ```  

6. Explore the visualizations and output files generated in the output directory.  



## Project Structure  

```
Big-Data-Project/  
├── data/                 
├── output/                
├── src/                   
│   ├── producer.py       
│   ├── consumer.py        
├── main.py                
├── README.md               
└── requirements.txt        
```  



## Example Video Processing  

### Kafka Producer Example:  
```python  
from kafka import KafkaProducer  
import cv2  

producer = KafkaProducer(bootstrap_servers='localhost:9092')  
video = cv2.VideoCapture('data/sample_video.mp4')  

while video.isOpened():  
    ret, frame = video.read()  
    if not ret:  
        break  
    producer.send('video-stream', frame.tobytes())  

video.release()  
producer.close()  
```  

### Kafka Consumer Example:  
```python  
from kafka import KafkaConsumer  
import cv2  
import numpy as np  

consumer = KafkaConsumer('video-stream', bootstrap_servers='localhost:9092')  

for message in consumer:  
    frame = np.frombuffer(message.value, dtype=np.uint8)  
    # Process the frame here  
    cv2.imshow('Video Frame', frame)  
    if cv2.waitKey(1) & 0xFF == ord('q'):  
        break  

cv2.destroyAllWindows()  
consumer.close()  
```  



## Contribution  

Contributions are welcome!  
- Fork the repository.  
- Submit a pull request with your improvements or features.  
- Report issues or bugs in the Issues section.  


## License  

This project is licensed under the MIT License.  



## Acknowledgments  

Special thanks to the open-source community and contributors of big data tools like Apache Hadoop, Apache Spark, Apache Kafka, and Python libraries for enabling seamless data processing and analysis.  

