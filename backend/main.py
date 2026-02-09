# import os
# from pathlib import Path
# import joblib
# import pandas as pd
# import logging
# import math
# from datetime import datetime
# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel, Field
# from fastapi.middleware.cors import CORSMiddleware
# from sklearn.metrics import confusion_matrix, roc_curve, roc_auc_score
# from sklearn.metrics import precision_score, recall_score, f1_score

# from fastapi import File, UploadFile
# from io import StringIO


# # Configure logging
# logging.basicConfig(
#     level=logging.INFO,
#     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#     handlers=[
#         logging.FileHandler('prediction_logs.log'),
#         logging.StreamHandler()
#     ]
# )
# logger = logging.getLogger(__name__)

# # Load model artifact
# BASE_DIR = Path(__file__).resolve().parent.parent
# ARTIFACT_PATH = BASE_DIR / "ml" / "artifacts" / "model.joblib"

# if not os.path.exists(ARTIFACT_PATH):
#     logger.error(f"Model not found at {ARTIFACT_PATH}")
#     raise FileNotFoundError(f"Model not found. Run train_and_export.py first.")

# logger.info("Loading model...")
# bundle = joblib.load(str(ARTIFACT_PATH))
# model = bundle["model"]
# base_rate = bundle.get("base_rate", 0.15)
# logger.info(f"Model loaded successfully. Base rate: {base_rate:.4f}")

# app = FastAPI(
#     title="Campaign Targeting API",
#     version="1.0.0",
#     description="Production-grade ML prediction API"
# )

# # CORS
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # Request counter for monitoring
# prediction_count = 0

# prediction_history = []

# # Helper function to sanitize JSON
# def sanitize_for_json(obj):
#     """Convert numpy/pandas types and handle inf/nan"""
#     import numpy as np
    
#     if isinstance(obj, dict):
#         return {k: sanitize_for_json(v) for k, v in obj.items()}
#     elif isinstance(obj, list):
#         return [sanitize_for_json(item) for item in obj]
#     elif isinstance(obj, (np.integer, np.int64, np.int32)):
#         return int(obj)
#     elif isinstance(obj, (np.floating, np.float64, np.float32, float)):
#         if math.isnan(obj) or math.isinf(obj):
#             return 0.0
#         return float(obj)
#     elif isinstance(obj, np.ndarray):
#         return sanitize_for_json(obj.tolist())
#     else:
#         return obj

# class PredictRequest(BaseModel):
#     Administrative: int = 0
#     Administrative_Duration: float = 0.0
#     Informational: int = 0
#     Informational_Duration: float = 0.0
#     ProductRelated: int = 1
#     ProductRelated_Duration: float = 0.0
#     BounceRates: float = 0.02
#     ExitRates: float = 0.05
#     PageValues: float = 0.0
#     SpecialDay: float = 0.0
#     Month: str = Field(default="May")
#     OperatingSystems: str = Field(default="2")
#     Browser: str = Field(default="2")
#     Region: str = Field(default="1")
#     TrafficType: str = Field(default="2")
#     VisitorType: str = Field(default="Returning_Visitor")
#     Weekend: bool = False

# class PredictResponse(BaseModel):
#     probability: float
#     decision: str
#     threshold: float
#     base_rate: float
#     prediction_id: str
#     timestamp: str
#     confidence_level: str 
#     risk_score: float 

# class HealthResponse(BaseModel):
#     status: str
#     model_loaded: bool
#     total_predictions: int
#     base_conversion_rate: float

# @app.get("/health", response_model=HealthResponse)
# def health():
#     """Health check endpoint with metrics"""
#     logger.info("Health check requested")
#     return {
#         "status": "ok",
#         "model_loaded": True,
#         "total_predictions": prediction_count,
#         "base_conversion_rate": float(base_rate)
#     }

# @app.get("/model-metrics")
# def model_metrics():
#     """Get model performance metrics"""
#     try:
#         data_path = BASE_DIR / "ml" / "data" / "online_shoppers_intention.csv"
        
#         if not os.path.exists(data_path):
#             return {"error": "Training data not found"}
        
#         import pandas as pd
#         import numpy as np
#         from sklearn.model_selection import train_test_split
        
#         logger.info("Calculating metrics...")
        
#         df = pd.read_csv(data_path)
#         df["Revenue"] = df["Revenue"].map({True: 1, False: 0}).astype(int)
        
#         X = df.drop(columns=["Revenue"])
#         y = df["Revenue"]
        
#         # ID columns to string
#         for c in ["OperatingSystems", "Browser", "Region", "TrafficType"]:
#             X[c] = X[c].astype(str)
        
#         _, X_test, _, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
        
#         probs = model.predict_proba(X_test)[:, 1]
#         preds = (probs >= 0.5).astype(int)
        
#         # Metrics
#         auc = roc_auc_score(y_test, probs)
#         cm = confusion_matrix(y_test, preds)
        
#         precision_1 = precision_score(y_test, preds, pos_label=1, zero_division=0)
#         recall_1 = recall_score(y_test, preds, pos_label=1, zero_division=0)
#         f1_1 = f1_score(y_test, preds, pos_label=1, zero_division=0)
        
#         # ROC curve
#         fpr, tpr, _ = roc_curve(y_test, probs)
#         step = max(1, len(fpr) // 50)
        
#         # Feature importance
#         feature_importance = None
#         if hasattr(model.named_steps['clf'], 'coef_'):
#             coef = np.nan_to_num(model.named_steps['clf'].coef_[0], nan=0, posinf=0, neginf=0)
            
#             num_feats = list(model.named_steps['prep'].transformers_[0][2])
#             cat_encoder = model.named_steps['prep'].named_transformers_['cat'].named_steps['onehot']
#             cat_feats = list(cat_encoder.get_feature_names_out(model.named_steps['prep'].transformers_[1][2]))
            
#             all_feats = num_feats + cat_feats
#             top_idx = np.argsort(np.abs(coef))[-20:][::-1]
            
#             feature_importance = {
#                 "features": [str(all_feats[i]) for i in top_idx],
#                 "importance": [coef[i] for i in top_idx]
#             }
        
#         result = {
#             "roc_auc": auc,
#             "confusion_matrix": cm.tolist(),
#             "roc_curve": {
#                 "fpr": fpr[::step].tolist(),
#                 "tpr": tpr[::step].tolist()
#             },
#             "classification_report": {
#                 "1": {
#                     "precision": precision_1,
#                     "recall": recall_1,
#                     "f1-score": f1_1
#                 }
#             },
#             "feature_importance": feature_importance,
#             "test_size": len(y_test),
#             "base_rate": base_rate
#         }
        
#         logger.info("Metrics calculated successfully")
        
#         # SANITIZE EVERYTHING before returning
#         return sanitize_for_json(result)
        
#     except Exception as e:
#         logger.error(f"Metrics failed: {e}", exc_info=True)
#         return {"error": str(e)}
# @app.post("/predict", response_model=PredictResponse)
# def predict(req: PredictRequest):
#     """Predict purchase probability"""
#     global prediction_count, prediction_history
#     prediction_count += 1
    
#     prediction_id = f"pred_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{prediction_count}"
    
#     logger.info(f"Prediction request {prediction_id}: VisitorType={req.VisitorType}, Month={req.Month}")
    
#     try:
#         x = pd.DataFrame([req.model_dump()])
        
#         for c in ["OperatingSystems", "Browser", "Region", "TrafficType"]:
#             x[c] = x[c].astype(str)
        
#         prob = float(model.predict_proba(x)[:, 1][0])
#         threshold = 0.50
#         decision = "TARGET" if prob >= threshold else "DO_NOT_TARGET"
        
#         # Calculate confidence level
#         distance_from_threshold = abs(prob - threshold)
#         if distance_from_threshold > 0.3:
#             confidence_level = "HIGH"
#         elif distance_from_threshold > 0.15:
#             confidence_level = "MEDIUM"
#         else:
#             confidence_level = "LOW"
        
#         # Calculate risk score (0-100)
#         if decision == "TARGET":
#             risk_score = (1 - prob) * 100  # Higher when probability is near threshold
#         else:
#             risk_score = prob * 100
        
#         logger.info(f"Prediction {prediction_id}: probability={prob:.4f}, decision={decision}, confidence={confidence_level}")

#         # Store in history (keep last 10)
#         history_entry = {
#             "prediction_id": prediction_id,
#             "timestamp": datetime.now().isoformat(),
#             "visitor_type": req.VisitorType,
#             "month": req.Month,
#             "probability": prob,
#             "decision": decision,
#             "type": "single"
#         }
#         prediction_history.insert(0, history_entry)  # Add to front
#         prediction_history = prediction_history[:10]  # Keep only last 10

#         return {
#             "probability": prob,
#             "decision": decision,
#             "threshold": threshold,
#             "base_rate": float(base_rate),
#             "prediction_id": prediction_id,
#             "timestamp": datetime.now().isoformat(),
#             "confidence_level": confidence_level,  # ADD THIS LINE
#             "risk_score": float(risk_score)        # ADD THIS LINE
#         }

    
#     except Exception as e:
#         logger.error(f"Prediction failed for {prediction_id}: {str(e)}")
#         raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")



# @app.get("/metrics")
# def metrics():
#     """Monitoring metrics endpoint"""
#     return {
#         "total_predictions": prediction_count,
#         "model_info": {
#             "base_rate": float(base_rate),
#             "threshold": 0.50
#         }
#     }


# @app.get("/history")
# def get_history():
#     """Get recent prediction history"""
#     return {
#         "history": prediction_history,
#         "count": len(prediction_history)
#     }

# @app.post("/predict-batch")
# async def predict_batch(file: UploadFile = File(...)):
#     """Batch prediction from CSV upload"""
#     global prediction_count  # ADD THIS LINE
#     try:
#         logger.info(f"Batch prediction requested: {file.filename}")
        
#         # Read uploaded CSV
#         contents = await file.read()
#         df = pd.read_csv(StringIO(contents.decode('utf-8')))
        
#         logger.info(f"Loaded {len(df)} rows from CSV")

#         prediction_count += len(df)  # ADD THIS LINE
        
#         # Ensure ID columns are strings
#         for c in ["OperatingSystems", "Browser", "Region", "TrafficType"]:
#             if c in df.columns:
#                 df[c] = df[c].astype(str)
        
#         # Predict
#         probs = model.predict_proba(df)[:, 1]
#         threshold = 0.50
#         decisions = ["TARGET" if p >= threshold else "DO_NOT_TARGET" for p in probs]
        
#         # Add predictions to dataframe
#         df['probability'] = probs
#         df['decision'] = decisions
        
#         # Convert to JSON-safe format
#         result = sanitize_for_json(df.to_dict(orient='records'))
        
#         logger.info(f"Batch prediction complete: {len(result)} predictions")
        
#         return {
#             "total_predictions": len(result),
#             "target_count": sum(1 for d in decisions if d == "TARGET"),
#             "predictions": result[:100]  # Limit to 100 for response size
#         }

#  @app.post("/simulate-ab-test")
# async def simulate_ab_test(file: UploadFile = File(...)):
#     """
#     A/B Test Simulator: Compare ML targeting vs Random/Baseline strategies
#     """
#     try:
#         logger.info(f"A/B test simulation requested: {file.filename}")
        
#         # Read uploaded CSV
#         contents = await file.read()
#         df = pd.read_csv(StringIO(contents.decode('utf-8')))
        
#         logger.info(f"Loaded {len(df)} rows for A/B simulation")
        
#         # Ensure ID columns are strings
#         for c in ["OperatingSystems", "Browser", "Region", "TrafficType"]:
#             if c in df.columns:
#                 df[c] = df[c].astype(str)
        
#         # Get ML predictions
#         probs = model.predict_proba(df)[:, 1]
        
#         # Campaign parameters (can be made configurable)
#         cost_per_contact = 1.0  # $1 per targeted visitor
#         revenue_per_conversion = 50.0  # $50 revenue per purchase
        
#         # Strategy A: ML Model (threshold = 0.5)
#         ml_threshold = 0.50
#         ml_targets = (probs >= ml_threshold).astype(int)
#         ml_contacted = ml_targets.sum()
#         ml_expected_conversions = probs[ml_targets == 1].sum()
#         ml_cost = ml_contacted * cost_per_contact
#         ml_revenue = ml_expected_conversions * revenue_per_conversion
#         ml_roi = ((ml_revenue - ml_cost) / ml_cost * 100) if ml_cost > 0 else 0
        
#         # Strategy B: Random Selection (contact same number as ML)
#         import numpy as np
#         np.random.seed(42)
#         random_targets = np.zeros(len(df), dtype=int)
#         if ml_contacted > 0:
#             random_indices = np.random.choice(len(df), size=min(ml_contacted, len(df)), replace=False)
#             random_targets[random_indices] = 1
#         random_contacted = random_targets.sum()
#         random_expected_conversions = probs[random_targets == 1].sum()
#         random_cost = random_contacted * cost_per_contact
#         random_revenue = random_expected_conversions * revenue_per_conversion
#         random_roi = ((random_revenue - random_cost) / random_cost * 100) if random_cost > 0 else 0
        
#         # Strategy C: Target Everyone (baseline)
#         all_contacted = len(df)
#         all_expected_conversions = probs.sum()
#         all_cost = all_contacted * cost_per_contact
#         all_revenue = all_expected_conversions * revenue_per_conversion
#         all_roi = ((all_revenue - all_cost) / all_cost * 100) if all_cost > 0 else 0
        
#         # Strategy D: Target No One (do nothing)
#         none_cost = 0
#         none_revenue = 0
#         none_roi = 0
        
#         # Calculate lift (ML vs Random)
#         lift = ((ml_roi - random_roi) / abs(random_roi) * 100) if random_roi != 0 else 0
        
#         result = {
#             "total_visitors": len(df),
#             "strategies": {
#                 "ml_model": {
#                     "name": "ML Model (Threshold 0.5)",
#                     "contacted": int(ml_contacted),
#                     "expected_conversions": float(ml_expected_conversions),
#                     "cost": float(ml_cost),
#                     "revenue": float(ml_revenue),
#                     "profit": float(ml_revenue - ml_cost),
#                     "roi": float(ml_roi),
#                     "conversion_rate": float(ml_expected_conversions / ml_contacted * 100) if ml_contacted > 0 else 0
#                 },
#                 "random": {
#                     "name": "Random Selection",
#                     "contacted": int(random_contacted),
#                     "expected_conversions": float(random_expected_conversions),
#                     "cost": float(random_cost),
#                     "revenue": float(random_revenue),
#                     "profit": float(random_revenue - random_cost),
#                     "roi": float(random_roi),
#                     "conversion_rate": float(random_expected_conversions / random_contacted * 100) if random_contacted > 0 else 0
#                 },
#                 "target_all": {
#                     "name": "Target Everyone",
#                     "contacted": int(all_contacted),
#                     "expected_conversions": float(all_expected_conversions),
#                     "cost": float(all_cost),
#                     "revenue": float(all_revenue),
#                     "profit": float(all_revenue - all_cost),
#                     "roi": float(all_roi),
#                     "conversion_rate": float(all_expected_conversions / all_contacted * 100) if all_contacted > 0 else 0
#                 },
#                 "target_none": {
#                     "name": "Target No One",
#                     "contacted": 0,
#                     "expected_conversions": 0,
#                     "cost": 0,
#                     "revenue": 0,
#                     "profit": 0,
#                     "roi": 0,
#                     "conversion_rate": 0
#                 }
#             },
#             "comparison": {
#                 "best_strategy": "ml_model" if ml_roi == max(ml_roi, random_roi, all_roi, none_roi) else "other",
#                 "ml_vs_random_lift": float(lift),
#                 "cost_per_contact": cost_per_contact,
#                 "revenue_per_conversion": revenue_per_conversion
#             }
#         }
        
#         logger.info(f"A/B simulation complete. ML ROI: {ml_roi:.2f}%, Random ROI: {random_roi:.2f}%")
        
#         return sanitize_for_json(result)
        
#     except Exception as e:
#         logger.error(f"A/B simulation failed: {str(e)}", exc_info=True)
#         raise HTTPException(status_code=400, detail=f"A/B simulation failed: {str(e)}")


# import os
# from pathlib import Path
# import joblib
# import pandas as pd
# import logging
# import math
# from datetime import datetime
# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel, Field
# from fastapi.middleware.cors import CORSMiddleware
# from sklearn.metrics import confusion_matrix, roc_curve, roc_auc_score
# from sklearn.metrics import precision_score, recall_score, f1_score
# from fastapi import File, UploadFile
# from io import StringIO

# # Configure logging
# logging.basicConfig(
#     level=logging.INFO,
#     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#     handlers=[
#         logging.FileHandler('prediction_logs.log'),
#         logging.StreamHandler()
#     ]
# )
# logger = logging.getLogger(__name__)

# # Load model artifact
# BASE_DIR = Path(__file__).resolve().parent.parent
# ARTIFACT_PATH = BASE_DIR / "ml" / "artifacts" / "model.joblib"

# if not os.path.exists(ARTIFACT_PATH):
#     logger.error(f"Model not found at {ARTIFACT_PATH}")
#     raise FileNotFoundError(f"Model not found. Run train_and_export.py first.")

# logger.info("Loading model...")
# bundle = joblib.load(str(ARTIFACT_PATH))
# model = bundle["model"]
# base_rate = bundle.get("base_rate", 0.15)
# logger.info(f"Model loaded successfully. Base rate: {base_rate:.4f}")

# app = FastAPI(
#     title="Campaign Targeting API",
#     version="1.0.0",
#     description="Production-grade ML prediction API"
# )

# # CORS
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # Request counter for monitoring
# prediction_count = 0
# prediction_history = []

# # Helper function to sanitize JSON
# def sanitize_for_json(obj):
#     """Convert numpy/pandas types and handle inf/nan"""
#     import numpy as np
    
#     if isinstance(obj, dict):
#         return {k: sanitize_for_json(v) for k, v in obj.items()}
#     elif isinstance(obj, list):
#         return [sanitize_for_json(item) for item in obj]
#     elif isinstance(obj, (np.integer, np.int64, np.int32)):
#         return int(obj)
#     elif isinstance(obj, (np.floating, np.float64, np.float32, float)):
#         if math.isnan(obj) or math.isinf(obj):
#             return 0.0
#         return float(obj)
#     elif isinstance(obj, np.ndarray):
#         return sanitize_for_json(obj.tolist())
#     else:
#         return obj

# class PredictRequest(BaseModel):
#     Administrative: int = 0
#     Administrative_Duration: float = 0.0
#     Informational: int = 0
#     Informational_Duration: float = 0.0
#     ProductRelated: int = 1
#     ProductRelated_Duration: float = 0.0
#     BounceRates: float = 0.02
#     ExitRates: float = 0.05
#     PageValues: float = 0.0
#     SpecialDay: float = 0.0
#     Month: str = Field(default="May")
#     OperatingSystems: str = Field(default="2")
#     Browser: str = Field(default="2")
#     Region: str = Field(default="1")
#     TrafficType: str = Field(default="2")
#     VisitorType: str = Field(default="Returning_Visitor")
#     Weekend: bool = False

# class PredictResponse(BaseModel):
#     probability: float
#     decision: str
#     threshold: float
#     base_rate: float
#     prediction_id: str
#     timestamp: str
#     confidence_level: str 
#     risk_score: float 

# class HealthResponse(BaseModel):
#     status: str
#     model_loaded: bool
#     total_predictions: int
#     base_conversion_rate: float

# @app.get("/health", response_model=HealthResponse)
# def health():
#     """Health check endpoint with metrics"""
#     logger.info("Health check requested")
#     return {
#         "status": "ok",
#         "model_loaded": True,
#         "total_predictions": prediction_count,
#         "base_conversion_rate": float(base_rate)
#     }

# @app.get("/model-metrics")
# def model_metrics():
#     """Get model performance metrics"""
#     try:
#         data_path = BASE_DIR / "ml" / "data" / "online_shoppers_intention.csv"
        
#         if not os.path.exists(data_path):
#             return {"error": "Training data not found"}
        
#         import pandas as pd
#         import numpy as np
#         from sklearn.model_selection import train_test_split
        
#         logger.info("Calculating metrics...")
        
#         df = pd.read_csv(data_path)
#         df["Revenue"] = df["Revenue"].map({True: 1, False: 0}).astype(int)
        
#         X = df.drop(columns=["Revenue"])
#         y = df["Revenue"]
        
#         # ID columns to string
#         for c in ["OperatingSystems", "Browser", "Region", "TrafficType"]:
#             X[c] = X[c].astype(str)
        
#         _, X_test, _, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
        
#         probs = model.predict_proba(X_test)[:, 1]
#         preds = (probs >= 0.5).astype(int)
        
#         # Metrics
#         auc = roc_auc_score(y_test, probs)
#         cm = confusion_matrix(y_test, preds)
        
#         precision_1 = precision_score(y_test, preds, pos_label=1, zero_division=0)
#         recall_1 = recall_score(y_test, preds, pos_label=1, zero_division=0)
#         f1_1 = f1_score(y_test, preds, pos_label=1, zero_division=0)
        
#         # ROC curve
#         fpr, tpr, _ = roc_curve(y_test, probs)
#         step = max(1, len(fpr) // 50)
        
#         # Feature importance
#         feature_importance = None
#         if hasattr(model.named_steps['clf'], 'coef_'):
#             coef = np.nan_to_num(model.named_steps['clf'].coef_[0], nan=0, posinf=0, neginf=0)
            
#             num_feats = list(model.named_steps['prep'].transformers_[0][2])
#             cat_encoder = model.named_steps['prep'].named_transformers_['cat'].named_steps['onehot']
#             cat_feats = list(cat_encoder.get_feature_names_out(model.named_steps['prep'].transformers_[1][2]))
            
#             all_feats = num_feats + cat_feats
#             top_idx = np.argsort(np.abs(coef))[-20:][::-1]
            
#             feature_importance = {
#                 "features": [str(all_feats[i]) for i in top_idx],
#                 "importance": [coef[i] for i in top_idx]
#             }
        
#         result = {
#             "roc_auc": auc,
#             "confusion_matrix": cm.tolist(),
#             "roc_curve": {
#                 "fpr": fpr[::step].tolist(),
#                 "tpr": tpr[::step].tolist()
#             },
#             "classification_report": {
#                 "1": {
#                     "precision": precision_1,
#                     "recall": recall_1,
#                     "f1-score": f1_1
#                 }
#             },
#             "feature_importance": feature_importance,
#             "test_size": len(y_test),
#             "base_rate": base_rate
#         }
        
#         logger.info("Metrics calculated successfully")
        
#         return sanitize_for_json(result)
        
#     except Exception as e:
#         logger.error(f"Metrics failed: {e}", exc_info=True)
#         return {"error": str(e)}

# @app.post("/predict", response_model=PredictResponse)
# def predict(req: PredictRequest):
#     """Predict purchase probability"""
#     global prediction_count, prediction_history
#     prediction_count += 1
    
#     prediction_id = f"pred_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{prediction_count}"
    
#     logger.info(f"Prediction request {prediction_id}: VisitorType={req.VisitorType}, Month={req.Month}")
    
#     try:
#         x = pd.DataFrame([req.model_dump()])
        
#         for c in ["OperatingSystems", "Browser", "Region", "TrafficType"]:
#             x[c] = x[c].astype(str)
        
#         prob = float(model.predict_proba(x)[:, 1][0])
#         threshold = 0.50
#         decision = "TARGET" if prob >= threshold else "DO_NOT_TARGET"
        
#         # Calculate confidence level
#         distance_from_threshold = abs(prob - threshold)
#         if distance_from_threshold > 0.3:
#             confidence_level = "HIGH"
#         elif distance_from_threshold > 0.15:
#             confidence_level = "MEDIUM"
#         else:
#             confidence_level = "LOW"
        
#         # Calculate risk score (0-100)
#         if decision == "TARGET":
#             risk_score = (1 - prob) * 100
#         else:
#             risk_score = prob * 100
        
#         logger.info(f"Prediction {prediction_id}: probability={prob:.4f}, decision={decision}, confidence={confidence_level}")

#         # Store in history (keep last 10)
#         history_entry = {
#             "prediction_id": prediction_id,
#             "timestamp": datetime.now().isoformat(),
#             "visitor_type": req.VisitorType,
#             "month": req.Month,
#             "probability": prob,
#             "decision": decision,
#             "type": "single"
#         }
#         prediction_history.insert(0, history_entry)
#         prediction_history = prediction_history[:10]

#         return {
#             "probability": prob,
#             "decision": decision,
#             "threshold": threshold,
#             "base_rate": float(base_rate),
#             "prediction_id": prediction_id,
#             "timestamp": datetime.now().isoformat(),
#             "confidence_level": confidence_level,
#             "risk_score": float(risk_score)
#         }
    
#     except Exception as e:
#         logger.error(f"Prediction failed for {prediction_id}: {str(e)}")
#         raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

# @app.get("/metrics")
# def metrics():
#     """Monitoring metrics endpoint"""
#     return {
#         "total_predictions": prediction_count,
#         "model_info": {
#             "base_rate": float(base_rate),
#             "threshold": 0.50
#         }
#     }

# @app.get("/history")
# def get_history():
#     """Get recent prediction history"""
#     return {
#         "history": prediction_history,
#         "count": len(prediction_history)
#     }

# @app.post("/predict-batch")
# async def predict_batch(file: UploadFile = File(...)):
#     """Batch prediction from CSV upload"""
#     global prediction_count
#     try:
#         logger.info(f"Batch prediction requested: {file.filename}")
        
#         # Read uploaded CSV
#         contents = await file.read()
#         df = pd.read_csv(StringIO(contents.decode('utf-8')))
        
#         logger.info(f"Loaded {len(df)} rows from CSV")

#         prediction_count += len(df)
        
#         # Ensure ID columns are strings
#         for c in ["OperatingSystems", "Browser", "Region", "TrafficType"]:
#             if c in df.columns:
#                 df[c] = df[c].astype(str)
        
#         # Predict
#         probs = model.predict_proba(df)[:, 1]
#         threshold = 0.50
#         decisions = ["TARGET" if p >= threshold else "DO_NOT_TARGET" for p in probs]
        
#         # Add predictions to dataframe
#         df['probability'] = probs
#         df['decision'] = decisions
        
#         # Convert to JSON-safe format
#         result = sanitize_for_json(df.to_dict(orient='records'))
        
#         logger.info(f"Batch prediction complete: {len(result)} predictions")
        
#         return {
#             "total_predictions": len(result),
#             "target_count": sum(1 for d in decisions if d == "TARGET"),
#             "predictions": result[:100]
#         }
        
#     except Exception as e:
#         logger.error(f"Batch prediction failed: {str(e)}", exc_info=True)
#         raise HTTPException(status_code=400, detail=f"Batch prediction failed: {str(e)}")

# @app.post("/simulate-ab-test")
# async def simulate_ab_test(file: UploadFile = File(...)):
#     """A/B Test Simulator: Compare ML targeting vs Random/Baseline strategies"""
#     try:
#         logger.info(f"A/B test simulation requested: {file.filename}")
        
#         # Read uploaded CSV
#         contents = await file.read()
#         df = pd.read_csv(StringIO(contents.decode('utf-8')))
        
#         logger.info(f"Loaded {len(df)} rows for A/B simulation")
        
#         # Ensure ID columns are strings
#         for c in ["OperatingSystems", "Browser", "Region", "TrafficType"]:
#             if c in df.columns:
#                 df[c] = df[c].astype(str)
        
#         # Get ML predictions
#         probs = model.predict_proba(df)[:, 1]
        
#         # Campaign parameters
#         cost_per_contact = 1.0
#         revenue_per_conversion = 50.0
        
#         # Strategy A: ML Model (threshold = 0.5)
#         ml_threshold = 0.50
#         ml_targets = (probs >= ml_threshold).astype(int)
#         ml_contacted = ml_targets.sum()
#         ml_expected_conversions = probs[ml_targets == 1].sum()
#         ml_cost = ml_contacted * cost_per_contact
#         ml_revenue = ml_expected_conversions * revenue_per_conversion
#         ml_roi = ((ml_revenue - ml_cost) / ml_cost * 100) if ml_cost > 0 else 0
        
#         # Strategy B: Random Selection
#         import numpy as np
#         np.random.seed(42)
#         random_targets = np.zeros(len(df), dtype=int)
#         if ml_contacted > 0:
#             random_indices = np.random.choice(len(df), size=min(ml_contacted, len(df)), replace=False)
#             random_targets[random_indices] = 1
#         random_contacted = random_targets.sum()
#         random_expected_conversions = probs[random_targets == 1].sum()
#         random_cost = random_contacted * cost_per_contact
#         random_revenue = random_expected_conversions * revenue_per_conversion
#         random_roi = ((random_revenue - random_cost) / random_cost * 100) if random_cost > 0 else 0
        
#         # Strategy C: Target Everyone
#         all_contacted = len(df)
#         all_expected_conversions = probs.sum()
#         all_cost = all_contacted * cost_per_contact
#         all_revenue = all_expected_conversions * revenue_per_conversion
#         all_roi = ((all_revenue - all_cost) / all_cost * 100) if all_cost > 0 else 0
        
#         # Strategy D: Target No One
#         none_cost = 0
#         none_revenue = 0
#         none_roi = 0
        
#         # Calculate lift
#         lift = ((ml_roi - random_roi) / abs(random_roi) * 100) if random_roi != 0 else 0
        
#         result = {
#             "total_visitors": len(df),
#             "strategies": {
#                 "ml_model": {
#                     "name": "ML Model (Threshold 0.5)",
#                     "contacted": int(ml_contacted),
#                     "expected_conversions": float(ml_expected_conversions),
#                     "cost": float(ml_cost),
#                     "revenue": float(ml_revenue),
#                     "profit": float(ml_revenue - ml_cost),
#                     "roi": float(ml_roi),
#                     "conversion_rate": float(ml_expected_conversions / ml_contacted * 100) if ml_contacted > 0 else 0
#                 },
#                 "random": {
#                     "name": "Random Selection",
#                     "contacted": int(random_contacted),
#                     "expected_conversions": float(random_expected_conversions),
#                     "cost": float(random_cost),
#                     "revenue": float(random_revenue),
#                     "profit": float(random_revenue - random_cost),
#                     "roi": float(random_roi),
#                     "conversion_rate": float(random_expected_conversions / random_contacted * 100) if random_contacted > 0 else 0
#                 },
#                 "target_all": {
#                     "name": "Target Everyone",
#                     "contacted": int(all_contacted),
#                     "expected_conversions": float(all_expected_conversions),
#                     "cost": float(all_cost),
#                     "revenue": float(all_revenue),
#                     "profit": float(all_revenue - all_cost),
#                     "roi": float(all_roi),
#                     "conversion_rate": float(all_expected_conversions / all_contacted * 100) if all_contacted > 0 else 0
#                 },
#                 "target_none": {
#                     "name": "Target No One",
#                     "contacted": 0,
#                     "expected_conversions": 0,
#                     "cost": 0,
#                     "revenue": 0,
#                     "profit": 0,
#                     "roi": 0,
#                     "conversion_rate": 0
#                 }
#             },
#             "comparison": {
#                 "best_strategy": "ml_model" if ml_roi == max(ml_roi, random_roi, all_roi, none_roi) else "other",
#                 "ml_vs_random_lift": float(lift),
#                 "cost_per_contact": cost_per_contact,
#                 "revenue_per_conversion": revenue_per_conversion
#             }
#         }
        
#         logger.info(f"A/B simulation complete. ML ROI: {ml_roi:.2f}%, Random ROI: {random_roi:.2f}%")
        
#         return sanitize_for_json(result)
        
#     except Exception as e:
#         logger.error(f"A/B simulation failed: {str(e)}", exc_info=True)
#         raise HTTPException(status_code=400, detail=f"A/B simulation failed: {str(e)}")




import os
from pathlib import Path
import joblib
import pandas as pd
import logging
import math
from datetime import datetime
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from fastapi.middleware.cors import CORSMiddleware
from sklearn.metrics import confusion_matrix, roc_curve, roc_auc_score
from sklearn.metrics import precision_score, recall_score, f1_score
from fastapi import File, UploadFile
from io import StringIO
from collections import defaultdict
from datetime import date

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('prediction_logs.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Load model artifact
BASE_DIR = Path(__file__).resolve().parent.parent
ARTIFACT_PATH = BASE_DIR / "ml" / "artifacts" / "model.joblib"

if not os.path.exists(ARTIFACT_PATH):
    logger.error(f"Model not found at {ARTIFACT_PATH}")
    raise FileNotFoundError(f"Model not found. Run train_and_export.py first.")

logger.info("Loading model...")
bundle = joblib.load(str(ARTIFACT_PATH))
model = bundle["model"]
base_rate = bundle.get("base_rate", 0.15)
logger.info(f"Model loaded successfully. Base rate: {base_rate:.4f}")

app = FastAPI(
    title="Campaign Targeting API",
    version="1.0.0",
    description="Production-grade ML prediction API"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://shivvit2019.github.io"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request counter for monitoring
prediction_count = 0
prediction_history = []

# ADD THIS: Live metrics tracking
live_metrics = {
    "total_predictions": 0,
    "target_count": 0,
    "dont_target_count": 0,
    "total_probability": 0.0,
    "high_confidence_count": 0,
    "medium_confidence_count": 0,
    "low_confidence_count": 0,
    "predictions_by_date": defaultdict(int),
    "predictions_by_hour": defaultdict(int),
    "avg_probabilities": [],
    "visitor_types": defaultdict(int),
    "months": defaultdict(int)
}

# Helper function to sanitize JSON
def sanitize_for_json(obj):
    """Convert numpy/pandas types and handle inf/nan"""
    import numpy as np
    
    if isinstance(obj, dict):
        return {k: sanitize_for_json(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [sanitize_for_json(item) for item in obj]
    elif isinstance(obj, (np.integer, np.int64, np.int32)):
        return int(obj)
    elif isinstance(obj, (np.floating, np.float64, np.float32, float)):
        if math.isnan(obj) or math.isinf(obj):
            return 0.0
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return sanitize_for_json(obj.tolist())
    else:
        return obj

class PredictRequest(BaseModel):
    Administrative: int = 0
    Administrative_Duration: float = 0.0
    Informational: int = 0
    Informational_Duration: float = 0.0
    ProductRelated: int = 1
    ProductRelated_Duration: float = 0.0
    BounceRates: float = 0.02
    ExitRates: float = 0.05
    PageValues: float = 0.0
    SpecialDay: float = 0.0
    Month: str = Field(default="May")
    OperatingSystems: str = Field(default="2")
    Browser: str = Field(default="2")
    Region: str = Field(default="1")
    TrafficType: str = Field(default="2")
    VisitorType: str = Field(default="Returning_Visitor")
    Weekend: bool = False

class PredictResponse(BaseModel):
    probability: float
    decision: str
    threshold: float
    base_rate: float
    prediction_id: str
    timestamp: str
    confidence_level: str 
    risk_score: float 

class HealthResponse(BaseModel):
    status: str
    model_loaded: bool
    total_predictions: int
    base_conversion_rate: float

@app.get("/health", response_model=HealthResponse)
def health():
    """Health check endpoint with metrics"""
    logger.info("Health check requested")
    return {
        "status": "ok",
        "model_loaded": True,
        "total_predictions": prediction_count,
        "base_conversion_rate": float(base_rate)
    }

@app.get("/model-metrics")
def model_metrics():
    """Get model performance metrics"""
    try:
        data_path = BASE_DIR / "ml" / "data" / "online_shoppers_intention.csv"
        
        if not os.path.exists(data_path):
            return {"error": "Training data not found"}
        
        import pandas as pd
        import numpy as np
        from sklearn.model_selection import train_test_split
        
        logger.info("Calculating metrics...")
        
        df = pd.read_csv(data_path)
        df["Revenue"] = df["Revenue"].map({True: 1, False: 0}).astype(int)
        
        X = df.drop(columns=["Revenue"])
        y = df["Revenue"]
        
        # ID columns to string
        for c in ["OperatingSystems", "Browser", "Region", "TrafficType"]:
            X[c] = X[c].astype(str)
        
        _, X_test, _, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
        
        probs = model.predict_proba(X_test)[:, 1]
        preds = (probs >= 0.5).astype(int)
        
        # Metrics
        auc = roc_auc_score(y_test, probs)
        cm = confusion_matrix(y_test, preds)
        
        precision_1 = precision_score(y_test, preds, pos_label=1, zero_division=0)
        recall_1 = recall_score(y_test, preds, pos_label=1, zero_division=0)
        f1_1 = f1_score(y_test, preds, pos_label=1, zero_division=0)
        
        # ROC curve
        fpr, tpr, _ = roc_curve(y_test, probs)
        step = max(1, len(fpr) // 50)
        
        # Feature importance
        feature_importance = None
        if hasattr(model.named_steps['clf'], 'coef_'):
            coef = np.nan_to_num(model.named_steps['clf'].coef_[0], nan=0, posinf=0, neginf=0)
            
            num_feats = list(model.named_steps['prep'].transformers_[0][2])
            cat_encoder = model.named_steps['prep'].named_transformers_['cat'].named_steps['onehot']
            cat_feats = list(cat_encoder.get_feature_names_out(model.named_steps['prep'].transformers_[1][2]))
            
            all_feats = num_feats + cat_feats
            top_idx = np.argsort(np.abs(coef))[-20:][::-1]
            
            feature_importance = {
                "features": [str(all_feats[i]) for i in top_idx],
                "importance": [coef[i] for i in top_idx]
            }
        
        result = {
            "roc_auc": auc,
            "confusion_matrix": cm.tolist(),
            "roc_curve": {
                "fpr": fpr[::step].tolist(),
                "tpr": tpr[::step].tolist()
            },
            "classification_report": {
                "1": {
                    "precision": precision_1,
                    "recall": recall_1,
                    "f1-score": f1_1
                }
            },
            "feature_importance": feature_importance,
            "test_size": len(y_test),
            "base_rate": base_rate
        }
        
        logger.info("Metrics calculated successfully")
        
        return sanitize_for_json(result)
        
    except Exception as e:
        logger.error(f"Metrics failed: {e}", exc_info=True)
        return {"error": str(e)}

@app.post("/predict", response_model=PredictResponse)
def predict(req: PredictRequest):
    """Predict purchase probability"""
    global prediction_count, prediction_history, live_metrics  # ADD live_metrics
    prediction_count += 1
    
    prediction_id = f"pred_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{prediction_count}"
    
    logger.info(f"Prediction request {prediction_id}: VisitorType={req.VisitorType}, Month={req.Month}")
    
    try:
        x = pd.DataFrame([req.model_dump()])
        
        for c in ["OperatingSystems", "Browser", "Region", "TrafficType"]:
            x[c] = x[c].astype(str)
        
        prob = float(model.predict_proba(x)[:, 1][0])
        threshold = 0.50
        decision = "TARGET" if prob >= threshold else "DO_NOT_TARGET"
        
        # Calculate confidence level
        distance_from_threshold = abs(prob - threshold)
        if distance_from_threshold > 0.3:
            confidence_level = "HIGH"
        elif distance_from_threshold > 0.15:
            confidence_level = "MEDIUM"
        else:
            confidence_level = "LOW"
        
        # Calculate risk score (0-100)
        if decision == "TARGET":
            risk_score = (1 - prob) * 100
        else:
            risk_score = prob * 100
        
        logger.info(f"Prediction {prediction_id}: probability={prob:.4f}, decision={decision}, confidence={confidence_level}")

        # Store in history (keep last 10)
        history_entry = {
            "prediction_id": prediction_id,
            "timestamp": datetime.now().isoformat(),
            "visitor_type": req.VisitorType,
            "month": req.Month,
            "probability": prob,
            "decision": decision,
            "type": "single"
        }
        prediction_history.insert(0, history_entry)
        prediction_history = prediction_history[:10]

        # ADD THIS: Track live metrics
        now = datetime.now()
        today = now.strftime("%Y-%m-%d")
        hour = now.hour
        
        live_metrics["total_predictions"] += 1
        if decision == "TARGET":
            live_metrics["target_count"] += 1
        else:
            live_metrics["dont_target_count"] += 1
        
        live_metrics["total_probability"] += prob
        live_metrics["avg_probabilities"].append(prob)
        
        if confidence_level == "HIGH":
            live_metrics["high_confidence_count"] += 1
        elif confidence_level == "MEDIUM":
            live_metrics["medium_confidence_count"] += 1
        else:
            live_metrics["low_confidence_count"] += 1
        
        live_metrics["predictions_by_date"][today] += 1
        live_metrics["predictions_by_hour"][hour] += 1
        live_metrics["visitor_types"][req.VisitorType] += 1
        live_metrics["months"][req.Month] += 1

        return {
            "probability": prob,
            "decision": decision,
            "threshold": threshold,
            "base_rate": float(base_rate),
            "prediction_id": prediction_id,
            "timestamp": datetime.now().isoformat(),
            "confidence_level": confidence_level,
            "risk_score": float(risk_score)
        }
    
    except Exception as e:
        logger.error(f"Prediction failed for {prediction_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

@app.get("/metrics")
def metrics():
    """Monitoring metrics endpoint"""
    return {
        "total_predictions": prediction_count,
        "model_info": {
            "base_rate": float(base_rate),
            "threshold": 0.50
        }
    }

@app.get("/history")
def get_history():
    """Get recent prediction history"""
    return {
        "history": prediction_history,
        "count": len(prediction_history)
    }

@app.get("/live-metrics")
def get_live_metrics():
    """Get real-time prediction metrics"""
    try:
        total = live_metrics["total_predictions"]
        
        # Calculate averages
        avg_probability = (live_metrics["total_probability"] / total) if total > 0 else 0
        target_rate = (live_metrics["target_count"] / total * 100) if total > 0 else 0
        
        # Get recent probability trend (last 20)
        recent_probs = live_metrics["avg_probabilities"][-20:] if live_metrics["avg_probabilities"] else []
        
        # Predictions by date (last 7 days)
        sorted_dates = sorted(live_metrics["predictions_by_date"].items(), reverse=True)[:7]
        predictions_by_date = {date: count for date, count in sorted_dates}
        
        # Predictions by hour (today)
        predictions_by_hour = dict(live_metrics["predictions_by_hour"])
        
        # Top visitor types
        visitor_types = dict(sorted(live_metrics["visitor_types"].items(), 
                                   key=lambda x: x[1], reverse=True)[:5])
        
        # Top months
        months = dict(sorted(live_metrics["months"].items(), 
                           key=lambda x: x[1], reverse=True)[:5])
        
        result = {
            "summary": {
                "total_predictions": total,
                "target_count": live_metrics["target_count"],
                "dont_target_count": live_metrics["dont_target_count"],
                "target_rate": target_rate,
                "avg_probability": avg_probability,
                "high_confidence": live_metrics["high_confidence_count"],
                "medium_confidence": live_metrics["medium_confidence_count"],
                "low_confidence": live_metrics["low_confidence_count"]
            },
            "trends": {
                "recent_probabilities": recent_probs,
                "predictions_by_date": predictions_by_date,
                "predictions_by_hour": predictions_by_hour
            },
            "segments": {
                "visitor_types": visitor_types,
                "months": months
            }
        }
        
        return sanitize_for_json(result)
        
    except Exception as e:
        logger.error(f"Live metrics failed: {str(e)}", exc_info=True)
        return {"error": str(e)}

@app.post("/predict-batch")
async def predict_batch(file: UploadFile = File(...)):
    """Batch prediction from CSV upload"""
    global prediction_count
    try:
        logger.info(f"Batch prediction requested: {file.filename}")
        
        # Read uploaded CSV
        contents = await file.read()
        df = pd.read_csv(StringIO(contents.decode('utf-8')))
        
        logger.info(f"Loaded {len(df)} rows from CSV")

        prediction_count += len(df)
        
        # Ensure ID columns are strings
        for c in ["OperatingSystems", "Browser", "Region", "TrafficType"]:
            if c in df.columns:
                df[c] = df[c].astype(str)
        
        # Predict
        probs = model.predict_proba(df)[:, 1]
        threshold = 0.50
        decisions = ["TARGET" if p >= threshold else "DO_NOT_TARGET" for p in probs]
        
        # Add predictions to dataframe
        df['probability'] = probs
        df['decision'] = decisions
        
        # Convert to JSON-safe format
        result = sanitize_for_json(df.to_dict(orient='records'))
        
        logger.info(f"Batch prediction complete: {len(result)} predictions")
        
        return {
            "total_predictions": len(result),
            "target_count": sum(1 for d in decisions if d == "TARGET"),
            "predictions": result[:100]
        }
        
    except Exception as e:
        logger.error(f"Batch prediction failed: {str(e)}", exc_info=True)
        raise HTTPException(status_code=400, detail=f"Batch prediction failed: {str(e)}")

@app.post("/simulate-ab-test")
async def simulate_ab_test(file: UploadFile = File(...)):
    """A/B Test Simulator: Compare ML targeting vs Random/Baseline strategies"""
    try:
        logger.info(f"A/B test simulation requested: {file.filename}")
        
        # Read uploaded CSV
        contents = await file.read()
        df = pd.read_csv(StringIO(contents.decode('utf-8')))
        
        logger.info(f"Loaded {len(df)} rows for A/B simulation")
        
        # Ensure ID columns are strings
        for c in ["OperatingSystems", "Browser", "Region", "TrafficType"]:
            if c in df.columns:
                df[c] = df[c].astype(str)
        
        # Get ML predictions
        probs = model.predict_proba(df)[:, 1]
        
        # Campaign parameters
        cost_per_contact = 1.0
        revenue_per_conversion = 50.0
        
        # Strategy A: ML Model (threshold = 0.5)
        ml_threshold = 0.50
        ml_targets = (probs >= ml_threshold).astype(int)
        ml_contacted = ml_targets.sum()
        ml_expected_conversions = probs[ml_targets == 1].sum()
        ml_cost = ml_contacted * cost_per_contact
        ml_revenue = ml_expected_conversions * revenue_per_conversion
        ml_roi = ((ml_revenue - ml_cost) / ml_cost * 100) if ml_cost > 0 else 0
        
        # Strategy B: Random Selection
        import numpy as np
        np.random.seed(42)
        random_targets = np.zeros(len(df), dtype=int)
        if ml_contacted > 0:
            random_indices = np.random.choice(len(df), size=min(ml_contacted, len(df)), replace=False)
            random_targets[random_indices] = 1
        random_contacted = random_targets.sum()
        random_expected_conversions = probs[random_targets == 1].sum()
        random_cost = random_contacted * cost_per_contact
        random_revenue = random_expected_conversions * revenue_per_conversion
        random_roi = ((random_revenue - random_cost) / random_cost * 100) if random_cost > 0 else 0
        
        # Strategy C: Target Everyone
        all_contacted = len(df)
        all_expected_conversions = probs.sum()
        all_cost = all_contacted * cost_per_contact
        all_revenue = all_expected_conversions * revenue_per_conversion
        all_roi = ((all_revenue - all_cost) / all_cost * 100) if all_cost > 0 else 0
        
        # Strategy D: Target No One
        none_cost = 0
        none_revenue = 0
        none_roi = 0
        
        # Calculate lift
        lift = ((ml_roi - random_roi) / abs(random_roi) * 100) if random_roi != 0 else 0
        
        result = {
            "total_visitors": len(df),
            "strategies": {
                "ml_model": {
                    "name": "ML Model (Threshold 0.5)",
                    "contacted": int(ml_contacted),
                    "expected_conversions": float(ml_expected_conversions),
                    "cost": float(ml_cost),
                    "revenue": float(ml_revenue),
                    "profit": float(ml_revenue - ml_cost),
                    "roi": float(ml_roi),
                    "conversion_rate": float(ml_expected_conversions / ml_contacted * 100) if ml_contacted > 0 else 0
                },
                "random": {
                    "name": "Random Selection",
                    "contacted": int(random_contacted),
                    "expected_conversions": float(random_expected_conversions),
                    "cost": float(random_cost),
                    "revenue": float(random_revenue),
                    "profit": float(random_revenue - random_cost),
                    "roi": float(random_roi),
                    "conversion_rate": float(random_expected_conversions / random_contacted * 100) if random_contacted > 0 else 0
                },
                "target_all": {
                    "name": "Target Everyone",
                    "contacted": int(all_contacted),
                    "expected_conversions": float(all_expected_conversions),
                    "cost": float(all_cost),
                    "revenue": float(all_revenue),
                    "profit": float(all_revenue - all_cost),
                    "roi": float(all_roi),
                    "conversion_rate": float(all_expected_conversions / all_contacted * 100) if all_contacted > 0 else 0
                },
                "target_none": {
                    "name": "Target No One",
                    "contacted": 0,
                    "expected_conversions": 0,
                    "cost": 0,
                    "revenue": 0,
                    "profit": 0,
                    "roi": 0,
                    "conversion_rate": 0
                }
            },
            "comparison": {
                "best_strategy": "ml_model" if ml_roi == max(ml_roi, random_roi, all_roi, none_roi) else "other",
                "ml_vs_random_lift": float(lift),
                "cost_per_contact": cost_per_contact,
                "revenue_per_conversion": revenue_per_conversion
            }
        }
        
        logger.info(f"A/B simulation complete. ML ROI: {ml_roi:.2f}%, Random ROI: {random_roi:.2f}%")
        
        return sanitize_for_json(result)
        
    except Exception as e:
        logger.error(f"A/B simulation failed: {str(e)}", exc_info=True)
        raise HTTPException(status_code=400, detail=f"A/B simulation failed: {str(e)}")
