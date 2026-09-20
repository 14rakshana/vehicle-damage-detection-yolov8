\# AI-Based Vehicle Damage Detection Using YOLOv8



\## Project Overview



This project presents an AI-based vehicle damage detection system using

YOLOv8n (YOLOv8 Nano). The system detects and localizes different types

of vehicle damage from an input image.



The project also includes an FPGA-based hardware acceleration component

for the computationally intensive CNN operations, particularly

convolution and Multiply-Accumulate (MAC) operations.



\## Objectives



\- Automatically detect vehicle damage from images.

\- Identify the type and location of the damage.

\- Train and evaluate a YOLOv8n object detection model.

\- Develop a simple Streamlit-based detection interface.

\- Implement CNN/MAC operations as an FPGA hardware accelerator.

\- Explore efficient edge-AI deployment.



\## Dataset



The project uses the CarDD (Car Damage Detection) dataset.



Dataset statistics used in this project:



\- Images: 4,000

\- Damage annotations: 8,740

\- Training images: 2,816

\- Validation images: 810

\- Test images: 374



\### Damage Classes



1\. Dent

2\. Scratch

3\. Crack

4\. Glass Shatter

5\. Lamp Broken

6\. Tire Flat



\## Technology Stack



\- Python

\- YOLOv8

\- Ultralytics

\- PyTorch

\- OpenCV

\- Streamlit

\- Git / GitHub

\- Verilog HDL / FPGA for hardware acceleration



\## System Workflow



Vehicle Image

&#x20;      |

&#x20;      v

Image Preprocessing

&#x20;      |

&#x20;      v

YOLOv8n

&#x20;      |

&#x20;      v

Feature Extraction

&#x20;      |

&#x20;      v

Object Detection

&#x20;      |

&#x20;      v

Damage Class + Bounding Box + Confidence

&#x20;      |

&#x20;      v

Streamlit Visualization



For hardware acceleration, the computationally intensive CNN

operations are targeted for FPGA implementation using MAC-based

processing.



\## Model



The project uses YOLOv8n, the Nano variant of YOLOv8.



YOLOv8n was selected because it provides a lightweight object

detection model suitable for experimentation with edge and hardware

acceleration.



The model produces:



\- Damage class

\- Bounding box

\- Confidence score



\## Training



The CarDD COCO annotations were converted into YOLO format before

training.



Training configuration:



\- Model: YOLOv8n

\- Image size: 640 x 640

\- Batch size: 8

\- Configured epochs: 15

\- Workers: 0



The initial training run was performed on a CPU and was stopped after

approximately two completed epochs because of the long training time.

Therefore, the current model should be considered a baseline/prototype

model.



\## Current Evaluation Results



The current checkpoint produced the following test-set results:



| Metric | Result |

|---|---:|

| Precision | 0.391 |

| Recall | 0.381 |

| mAP@50 | 0.362 |

| mAP@50-95 | 0.246 |

| Inference time | \~43.6 ms/image |



These values represent the current prototype checkpoint and are not

intended to represent a fully optimized final model.



\## Streamlit Application



A Streamlit interface is provided for testing the trained model.



The application allows the user to:



1\. Upload a vehicle image.

2\. Select a confidence threshold.

3\. Run YOLOv8n inference.

4\. View detected damage bounding boxes.

5\. View damage classes and confidence values.

6\. View inference information.



\## FPGA Hardware Acceleration



The hardware component focuses on accelerating the computationally

intensive operations used by CNNs.



The proposed implementation consists of:



\- Input memory / BRAM

\- Fixed-point or INT8 data representation

\- Parallel MAC units

\- Accumulator

\- Control unit

\- Output registers



Conceptually:



Input Data

&#x20;   |

&#x20;   v

Input Memory

&#x20;   |

&#x20;   v

Parallel MAC Array

&#x20;   |

&#x20;   v

Accumulator

&#x20;   |

&#x20;   v

Output



The FPGA implementation is intended to demonstrate how CNN computation

can be mapped onto dedicated hardware for edge-AI applications.



\## Project Structure



```text

CarDamageAI/

│

├── app.py

├── convert\_cardd.py

├── dataset/

│   └── data.yaml

├── .gitignore

└── .gitattributes

