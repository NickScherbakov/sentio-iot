"""
Sentio IoT AI Engine
Provides anomaly detection, predictive maintenance, and intelligent alerting
"""
import os
import time
import logging
import json
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import joblib
import requests
import redis
import schedule

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuration
VICTORIAMETRICS_URL = os.getenv('VICTORIAMETRICS_URL', 'http://victoriametrics:8428')
REDIS_URL = os.getenv('REDIS_URL', 'redis://redis:6379')
MODEL_PATH = os.getenv('MODEL_PATH', '/app/models')

# Connect to Redis
redis_client = redis.from_url(REDIS_URL, decode_responses=True)


class AnomalyDetector:
    """Detects anomalies in metrics using machine learning"""
    
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self.model_path = os.path.join(MODEL_PATH, 'anomaly_detector.pkl')
        self.contamination = 0.1  # Expected proportion of outliers
        self.load_model()
    
    def load_model(self):
        """Load pre-trained model or create new one"""
        try:
            if os.path.exists(self.model_path):
                self.model = joblib.load(self.model_path)
                logger.info("Loaded pre-trained anomaly detection model")
            else:
                self.model = IsolationForest(
                    contamination=self.contamination,
                    random_state=42,
                    n_estimators=100
                )
                logger.info("Initialized new anomaly detection model")
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            self.model = IsolationForest(
                contamination=self.contamination,
                random_state=42,
                n_estimators=100
            )
    
    def save_model(self):
        """Save trained model to disk"""
        try:
            os.makedirs(MODEL_PATH, exist_ok=True)
            joblib.dump(self.model, self.model_path)
            logger.info("Saved anomaly detection model")
        except Exception as e:
            logger.error(f"Error saving model: {e}")
    
    def train(self, data: pd.DataFrame):
        """Train the anomaly detection model"""
        try:
            if data.empty or len(data) < 10:
                logger.warning("Insufficient data for training")
                return
            
            # Prepare features
            features = self._prepare_features(data)
            
            # Scale features
            features_scaled = self.scaler.fit_transform(features)
            
            # Train model
            self.model.fit(features_scaled)
            
            # Save model
            self.save_model()
            
            logger.info(f"Trained anomaly detection model on {len(data)} samples")
        
        except Exception as e:
            logger.error(f"Error training model: {e}")
    
    def detect(self, data: pd.DataFrame) -> List[Dict[str, Any]]:
        """Detect anomalies in the data"""
        try:
            if data.empty:
                return []
            
            # Prepare features
            features = self._prepare_features(data)
            
            # Scale features
            features_scaled = self.scaler.transform(features)
            
            # Predict anomalies (-1 for anomaly, 1 for normal)
            predictions = self.model.predict(features_scaled)
            
            # Get anomaly scores
            scores = self.model.score_samples(features_scaled)
            
            # Extract anomalies
            anomalies = []
            for i, (pred, score) in enumerate(zip(predictions, scores)):
                if pred == -1:
                    anomaly = {
                        'timestamp': data.iloc[i]['timestamp'],
                        'value': float(data.iloc[i]['value']),
                        'score': float(score),
                        'metric': data.iloc[i].get('metric', 'unknown')
                    }
                    anomalies.append(anomaly)
            
            logger.info(f"Detected {len(anomalies)} anomalies in {len(data)} samples")
            return anomalies
        
        except Exception as e:
            logger.error(f"Error detecting anomalies: {e}")
            return []
    
    def _prepare_features(self, data: pd.DataFrame) -> np.ndarray:
        """Prepare features for the model"""
        # Simple feature extraction - can be extended
        features = []
        for _, row in data.iterrows():
            feature_vector = [
                row.get('value', 0),
                # Add more features as needed
            ]
            features.append(feature_vector)
        return np.array(features)


class PredictiveMaintenanceEngine:
    """Predicts potential faults and failures"""
    
    def __init__(self):
        self.model = None
        self.model_path = os.path.join(MODEL_PATH, 'predictive_maintenance.pkl')
        self.lookback_days = 7
    
    def predict_failures(self, device_id: str, metrics: pd.DataFrame) -> Dict[str, Any]:
        """Predict potential failures for a device"""
        try:
            if metrics.empty or len(metrics) < 10:
                return {
                    'device_id': device_id,
                    'risk_level': 'unknown',
                    'confidence': 0.0,
                    'estimated_time_to_failure': None
                }
            
            # Calculate statistical features
            recent_values = metrics['value'].tail(100)
            
            # Compute health indicators
            mean_value = recent_values.mean()
            std_value = recent_values.std()
            trend = self._calculate_trend(recent_values)
            volatility = std_value / mean_value if mean_value != 0 else 0
            
            # Simple rule-based prediction (can be replaced with ML model)
            risk_level = 'low'
            confidence = 0.5
            
            if volatility > 0.5 or abs(trend) > 0.1:
                risk_level = 'high'
                confidence = 0.8
            elif volatility > 0.3 or abs(trend) > 0.05:
                risk_level = 'medium'
                confidence = 0.7
            
            # Estimate time to failure (simplified)
            estimated_ttf = None
            if risk_level == 'high':
                estimated_ttf = '1-3 days'
            elif risk_level == 'medium':
                estimated_ttf = '1-2 weeks'
            
            result = {
                'device_id': device_id,
                'risk_level': risk_level,
                'confidence': confidence,
                'estimated_time_to_failure': estimated_ttf,
                'indicators': {
                    'volatility': float(volatility),
                    'trend': float(trend),
                    'mean': float(mean_value),
                    'std': float(std_value)
                }
            }
            
            logger.info(f"Predicted failure risk for {device_id}: {risk_level}")
            return result
        
        except Exception as e:
            logger.error(f"Error predicting failures: {e}")
            return {
                'device_id': device_id,
                'risk_level': 'error',
                'confidence': 0.0,
                'estimated_time_to_failure': None
            }
    
    @staticmethod
    def _calculate_trend(values: pd.Series) -> float:
        """Calculate linear trend of values"""
        try:
            x = np.arange(len(values))
            z = np.polyfit(x, values, 1)
            return z[0]  # Slope
        except:
            return 0.0


class IntelligentAlertingSystem:
    """Manages intelligent alerting with context and priority"""
    
    def __init__(self):
        self.alert_threshold = 0.8
        self.cooldown_period = 300  # 5 minutes
    
    def evaluate_alert(self, anomalies: List[Dict[str, Any]], predictions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Evaluate and generate intelligent alerts"""
        alerts = []
        
        try:
            # Process anomalies
            for anomaly in anomalies:
                alert_score = abs(anomaly['score'])
                
                if alert_score > self.alert_threshold:
                    # Check if alert was recently sent (cooldown)
                    alert_key = f"alert:{anomaly['metric']}:{anomaly['timestamp']}"
                    if not self._is_in_cooldown(alert_key):
                        alert = {
                            'type': 'anomaly',
                            'severity': self._calculate_severity(alert_score),
                            'title': f"Anomaly detected in {anomaly['metric']}",
                            'description': f"Unusual value detected: {anomaly['value']}",
                            'timestamp': anomaly['timestamp'],
                            'score': alert_score,
                            'metric': anomaly['metric']
                        }
                        alerts.append(alert)
                        self._set_cooldown(alert_key)
            
            # Process predictions
            for prediction in predictions:
                if prediction['risk_level'] in ['high', 'medium']:
                    alert_key = f"alert:prediction:{prediction['device_id']}"
                    if not self._is_in_cooldown(alert_key):
                        alert = {
                            'type': 'prediction',
                            'severity': 'high' if prediction['risk_level'] == 'high' else 'medium',
                            'title': f"Potential failure predicted for {prediction['device_id']}",
                            'description': f"Risk level: {prediction['risk_level']}, Estimated TTF: {prediction.get('estimated_time_to_failure', 'unknown')}",
                            'timestamp': datetime.utcnow().isoformat(),
                            'confidence': prediction['confidence'],
                            'device_id': prediction['device_id']
                        }
                        alerts.append(alert)
                        self._set_cooldown(alert_key)
            
            logger.info(f"Generated {len(alerts)} intelligent alerts")
            return alerts
        
        except Exception as e:
            logger.error(f"Error evaluating alerts: {e}")
            return []
    
    def _calculate_severity(self, score: float) -> str:
        """Calculate alert severity based on score"""
        if score > 0.9:
            return 'critical'
        elif score > 0.8:
            return 'high'
        elif score > 0.6:
            return 'medium'
        else:
            return 'low'
    
    def _is_in_cooldown(self, alert_key: str) -> bool:
        """Check if alert is in cooldown period"""
        try:
            return redis_client.exists(alert_key) > 0
        except:
            return False
    
    def _set_cooldown(self, alert_key: str):
        """Set cooldown for alert"""
        try:
            redis_client.setex(alert_key, self.cooldown_period, '1')
        except Exception as e:
            logger.error(f"Error setting cooldown: {e}")


class AIEngine:
    """Main AI engine orchestrator"""
    
    def __init__(self):
        self.anomaly_detector = AnomalyDetector()
        self.predictive_maintenance = PredictiveMaintenanceEngine()
        self.alerting_system = IntelligentAlertingSystem()
    
    def fetch_metrics(self, query: str, hours: int = 1) -> pd.DataFrame:
        """Fetch metrics from VictoriaMetrics"""
        try:
            end_time = datetime.utcnow()
            start_time = end_time - timedelta(hours=hours)
            
            params = {
                'query': query,
                'start': int(start_time.timestamp()),
                'end': int(end_time.timestamp()),
                'step': '15s'
            }
            
            response = requests.get(
                f"{VICTORIAMETRICS_URL}/api/v1/query_range",
                params=params,
                timeout=30
            )
            response.raise_for_status()
            
            data = response.json()
            
            # Parse response and create DataFrame
            metrics = []
            for result in data.get('data', {}).get('result', []):
                metric_name = result.get('metric', {}).get('__name__', 'unknown')
                for timestamp, value in result.get('values', []):
                    try:
                        metrics.append({
                            'timestamp': datetime.fromtimestamp(timestamp).isoformat(),
                            'metric': metric_name,
                            'value': float(value)
                        })
                    except (ValueError, TypeError):
                        continue
            
            return pd.DataFrame(metrics)
        
        except Exception as e:
            logger.error(f"Error fetching metrics: {e}")
            return pd.DataFrame()
    
    def run_analysis(self):
        """Run full AI analysis pipeline"""
        try:
            logger.info("Starting AI analysis pipeline")
            
            # Fetch metrics (example query - adjust based on your metrics)
            metrics = self.fetch_metrics('{__name__=~".+"}', hours=1)
            
            if metrics.empty:
                logger.warning("No metrics available for analysis")
                return
            
            # Detect anomalies
            anomalies = self.anomaly_detector.detect(metrics)
            
            # Store anomalies in Redis
            if anomalies:
                redis_client.setex(
                    'ai:anomalies',
                    3600,  # 1 hour TTL
                    json.dumps(anomalies)
                )
            
            # Get unique devices/metrics for prediction
            unique_metrics = metrics['metric'].unique()[:10]  # Limit to 10 for demo
            predictions = []
            
            for metric in unique_metrics:
                metric_data = metrics[metrics['metric'] == metric]
                prediction = self.predictive_maintenance.predict_failures(metric, metric_data)
                predictions.append(prediction)
            
            # Store predictions in Redis
            if predictions:
                redis_client.setex(
                    'ai:predictions',
                    3600,  # 1 hour TTL
                    json.dumps(predictions)
                )
            
            # Generate intelligent alerts
            alerts = self.alerting_system.evaluate_alert(anomalies, predictions)
            
            # Store alerts in Redis
            if alerts:
                redis_client.setex(
                    'ai:alerts',
                    3600,  # 1 hour TTL
                    json.dumps(alerts)
                )
            
            logger.info(f"Analysis complete: {len(anomalies)} anomalies, {len(predictions)} predictions, {len(alerts)} alerts")
        
        except Exception as e:
            logger.error(f"Error running analysis: {e}")
    
    def train_models(self):
        """Periodic model training"""
        try:
            logger.info("Starting model training")
            
            # Fetch historical data (7 days)
            metrics = self.fetch_metrics('{__name__=~".+"}', hours=168)
            
            if not metrics.empty:
                self.anomaly_detector.train(metrics)
                logger.info("Model training complete")
            else:
                logger.warning("Insufficient data for training")
        
        except Exception as e:
            logger.error(f"Error training models: {e}")


def main():
    """Main entry point"""
    logger.info("Starting Sentio IoT AI Engine")
    
    # Initialize AI engine
    engine = AIEngine()
    
    # Schedule periodic tasks
    schedule.every(5).minutes.do(engine.run_analysis)
    schedule.every().day.at("02:00").do(engine.train_models)
    
    # Run initial analysis
    engine.run_analysis()
    
    # Main loop
    while True:
        schedule.run_pending()
        time.sleep(60)


if __name__ == '__main__':
    main()
