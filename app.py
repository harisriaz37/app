# from fastapi import FastAPI, UploadFile, File
# from fastapi.responses import HTMLResponse, StreamingResponse
# from fastapi.staticfiles import StaticFiles
# from fastapi.templating import Jinja2Templates
# import uvicorn
# import cv2
# from ultralytics import YOLO
# import numpy as np
# from io import BytesIO
# from PIL import Image

# app = FastAPI()

# # Mount static directory for CSS files
# app.mount("/static", StaticFiles(directory="static"), name="static")

# # Jinja2 templates for rendering HTML
# templates = Jinja2Templates(directory="templates")

# # Load your YOLO model
# model = YOLO('best.pt')

# # Route to serve the HTML page
# @app.get("/", response_class=HTMLResponse)
# async def main():
#     return templates.TemplateResponse("index.html", {"request": {}})

# # Route to handle image upload and prediction
# @app.post("/predict/")
# async def predict(file: UploadFile = File(...)):
#     contents = await file.read()

#     # Convert the uploaded image to OpenCV format
#     image = np.array(Image.open(BytesIO(contents)).convert("RGB"))
#     image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)  # Convert to BGR format for OpenCV

#     # Run the YOLO model
#     outputs = model.predict(source=image)
#     results = outputs[0]

#     # Draw bounding boxes on the image
#     for i, det in enumerate(results.boxes.xyxy):
#         x1, y1, x2, y2 = map(int, det[:4])
#         class_id = int(results.boxes.cls[i])
#         class_name = results.names[class_id]

#         # Draw the bounding box
#         cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
#         cv2.putText(image, class_name, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

#     # Convert the image back to RGB for returning
#     _, buffer = cv2.imencode('.jpg', image)
#     return StreamingResponse(BytesIO(buffer), media_type="image/jpeg")

# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000) 

from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse, StreamingResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
import cv2
from ultralytics import YOLO
import numpy as np
from io import BytesIO
from PIL import Image

app = FastAPI()

# Mount static directory for CSS files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Jinja2 templates for rendering HTML
templates = Jinja2Templates(directory="templates")

# Load your YOLO model
model = YOLO('best.pt')

# Route to serve the HTML page
@app.get("/", response_class=HTMLResponse)
async def main():
    return templates.TemplateResponse("index.html", {"request": {}})

# Route to handle image upload and prediction
@app.post("/predict/")
async def predict(file: UploadFile = File(...)):
    contents = await file.read()

    # Convert the uploaded image to OpenCV format
    image = np.array(Image.open(BytesIO(contents)).convert("RGB"))
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)  # Convert to BGR format for OpenCV

    # Run the YOLO model
    outputs = model.predict(source=image)
    results = outputs[0]

    # Check if any waste was detected
    if len(results.boxes) == 0:
        return JSONResponse(content={"message": "No waste found"})

    # Draw bounding boxes on the image
    for i, det in enumerate(results.boxes.xyxy):
        x1, y1, x2, y2 = map(int, det[:4])
        class_id = int(results.boxes.cls[i])
        class_name = results.names[class_id]

        # Draw the bounding box
        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(image, class_name, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

    # Convert the image back to RGB for returning
    _, buffer = cv2.imencode('.jpg', image)
    return StreamingResponse(BytesIO(buffer), media_type="image/jpeg")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)