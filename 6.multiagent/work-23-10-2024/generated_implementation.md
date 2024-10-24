```python
from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np
from scipy import stats

app = FastAPI()

class DataInput(BaseModel):
    count: int
    mean: float
    std_dev: float

@app.post("/generate-data/")
def generate_data(data: DataInput):
    # Generate normally distributed data
    generated_data = np.random.normal(data.mean, data.std_dev, data.count)

    # Calculate mean and standard deviation
    mean = np.mean(generated_data)
    std_dev = np.std(generated_data)

    # Perform a statistical test (one-sample t-test against population mean = 0)
    t_stat, p_value = stats.ttest_1samp(generated_data, 0)

    return {
        "mean": mean,
        "std_dev": std_dev,
        "t_statistic": t_stat,
        "p_value": p_value,
        "data": generated_data.tolist()  # Convert to list for JSON serialization
    }

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI SciPy application. Use the /generate-data endpoint to generate and analyze normally distributed data."}
```

This code implements a simple FastAPI application that accepts user input for generating normally distributed data. The user must specify the number of data points, mean, and standard deviation through a POST request to the `/generate-data/` endpoint. The application then calculates the mean, standard deviation, and performs a one-sample t-test on the generated data, returning these statistics in the response. 

To run this application, save the code in a file named `main.py` and execute it with the command:

```bash
uvicorn main:app --reload
```

After running, you can make POST requests to `http://127.0.0.1:8000/generate-data/` with a JSON body like:

```json
{
    "count": 1000,
    "mean": 0,
    "std_dev": 1
}
```

You will receive a response that includes the mean, standard deviation, t-statistic, p-value, and the generated data itself (as a list). The `/` endpoint provides a welcome message for users of the API.