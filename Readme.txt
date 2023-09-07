# Recommendation System

This project presents an end-to-end recommendation system designed for an e-commerce platform. The system utilizes item-based collaborative filtering using the Surprise library for recommendation generation and Flask for creating APIs for easy integration into Android apps or websites.

## Implementation Details

### 1. Main Driver - `myapp.py`
- This is the core of the project, serving as the main driver file.
- It configures and deploys the Flask API, making it ready for use on IIS servers.

### 2. Similarity Matrix Calculation - `InsertRecSys.py`
- This program is responsible for calculating the similarity matrix based on user-item interactions.
- It then inserts this matrix into a MongoDB database for later use in recommendation generation.

### 3. Recommendation Generation - `RecSys.py` and `RecSys2.py`
- `RecSys.py`:
  - These programs generate top-N recommendations by reading and utilizing the similarity matrix stored in the MongoDB database.
  - Users can specify the item ID and the number of recommendations they desire as parameters in the API.

- `RecSys2.py`:
  - Similar to `RecSys.py`, these programs generate top-N recommendations from the MongoDB database using the similarity matrix.
  - In addition to item ID and the number of recommendations, users can also provide a warehouse ID (wid) parameter to restrict recommendations to items available in their city's warehouse.

## Evaluation
- The recommender system has been rigorously evaluated using Leave-One-Out (LOO) Cross Validation.
- Achieved a hit rate of 21%, which is considered quite good in the context of recommendation systems.

## Usage
To leverage the recommendation system and its APIs, follow these steps:

1. Ensure you have the necessary dependencies installed, including Flask, Surprise, and MongoDB drivers.
2. Run `myapp.py` to configure and deploy the Flask API.
3. Calculate and insert the similarity matrix into MongoDB using `InsertRecSys.py`.
4. Utilize the recommendation APIs (`RecSys.py` and `RecSys2.py`) in your Android app or website by passing the appropriate parameters for item ID, number of recommendations, and, if needed, the warehouse ID.

## Acknowledgments
This project showcases the power of item-based collaborative filtering and Flask APIs for enhancing user experience on your e-commerce platform.
