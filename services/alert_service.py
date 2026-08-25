from models.alert_model import AlertModel

class AlertService:
    @staticmethod
    def check_and_generate_alerts(farm_id, observation, recommendations=None):
        """
        Evaluate recent telemetry parameters and agent suggestions,
        automatically issuing alerts where threshold anomalies are found.
        """
        alerts_created = 0

        # 1. Telemetry Moisture Check
        if observation:
            moisture = observation.get('soil_moisture')
            if moisture is not None:
                if moisture < 30.0:
                    AlertModel.create(
                        farm_id=farm_id,
                        severity='HIGH',
                        title='Critical Soil Moisture Deficit',
                        description=f'Soil moisture has dropped to {moisture}%. Urgent irrigation scheduling recommended.'
                    )
                    alerts_created += 1
                elif moisture > 80.0:
                    AlertModel.create(
                        farm_id=farm_id,
                        severity='MEDIUM',
                        title='Elevated Soil Moisture Levels',
                        description=f'Soil moisture is high at {moisture}%. Risk of root saturations or fungal diseases.'
                    )
                    alerts_created += 1

            # 2. Telemetry pH Level Check
            ph = observation.get('soil_ph')
            if ph is not None:
                if ph < 5.5:
                    AlertModel.create(
                        farm_id=farm_id,
                        severity='MEDIUM',
                        title='Acidic Soil Anomaly',
                        description=f'Soil pH has fallen to acidic levels ({ph}). Liming options should be reviewed.'
                    )
                    alerts_created += 1
                elif ph > 7.8:
                    AlertModel.create(
                        farm_id=farm_id,
                        severity='MEDIUM',
                        title='Alkaline Soil Anomaly',
                        description=f'Soil pH has risen to alkaline levels ({ph}). Acidifying compost application recommended.'
                    )
                    alerts_created += 1

            # 3. Crop Health Status Check
            health = observation.get('crop_health')
            if health is not None:
                if health < 70.0:
                    AlertModel.create(
                        farm_id=farm_id,
                        severity='HIGH',
                        title='Critical Crop Decline Detected',
                        description=f'Crop health index is dangerously low at {health}%. Trigger disease diagnostic runs immediately.'
                    )
                    alerts_created += 1

        # 4. Agent Recommendations Priority check
        if recommendations:
            for rec in recommendations:
                if rec.get('priority') == 'High':
                    AlertModel.create(
                        farm_id=farm_id,
                        severity='HIGH',
                        title=f"Critical Alert: {rec.get('title')}",
                        description=f"Action required from {rec.get('agent_name')}: {rec.get('description')}"
                    )
                    alerts_created += 1

        return alerts_created
