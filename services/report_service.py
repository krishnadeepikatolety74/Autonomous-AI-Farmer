import io
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

class ReportService:
    @staticmethod
    def generate_pdf(farm, crop, observation, recommendations, alerts, recent_runs, final_plan=None):
        """
        Compile farm details and AI planner outputs, writing a clean,
        professional layout PDF using reportlab.
        """
        buffer = io.BytesIO()
        
        # Setup document properties
        doc = SimpleDocTemplate(
            buffer, 
            pagesize=letter,
            rightMargin=54, leftMargin=54, topMargin=54, bottomMargin=54
        )
        
        story = []
        styles = getSampleStyleSheet()
        
        # Custom styles using our SaaS forest-green theme palette
        primary_color = colors.HexColor("#285943")    # Deep Forest
        secondary_color = colors.HexColor("#6FAF7B")  # Primary Green
        neutral_dark = colors.HexColor("#333333")     # Dark Charcoal
        bg_light = colors.HexColor("#F7FBF7")         # Pale Green background
        
        title_style = ParagraphStyle(
            'ReportTitle',
            parent=styles['Heading1'],
            fontName='Helvetica-Bold',
            fontSize=24,
            leading=28,
            textColor=primary_color,
            spaceAfter=15
        )
        
        h1_style = ParagraphStyle(
            'SectionHeading',
            parent=styles['Heading2'],
            fontName='Helvetica-Bold',
            fontSize=15,
            leading=18,
            textColor=primary_color,
            spaceBefore=14,
            spaceAfter=8,
            keepWithNext=True
        )

        h2_style = ParagraphStyle(
            'SubSectionHeading',
            parent=styles['Heading3'],
            fontName='Helvetica-Bold',
            fontSize=11,
            leading=14,
            textColor=secondary_color,
            spaceBefore=8,
            spaceAfter=4,
            keepWithNext=True
        )
        
        body_style = ParagraphStyle(
            'ReportBody',
            parent=styles['BodyText'],
            fontName='Helvetica',
            fontSize=10,
            leading=14,
            textColor=neutral_dark,
            spaceAfter=6
        )

        meta_style = ParagraphStyle(
            'ReportMeta',
            parent=styles['Normal'],
            fontName='Helvetica-Oblique',
            fontSize=9,
            leading=11,
            textColor=colors.HexColor("#666666"),
            spaceAfter=12
        )
        
        # 1. Header Section
        story.append(Paragraph("🌱 AUTONOMOUS AI FARMER", h2_style))
        story.append(Paragraph("Intelligent Digital Farm Report", title_style))
        story.append(Paragraph(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", meta_style))
        story.append(Spacer(1, 10))
        
        # 2. Farm and Crop Details (rendered as Table)
        story.append(Paragraph("1. Farm & Crop Specifications", h1_style))
        
        farm_name = farm.get('name') if farm else 'Unspecified'
        location = farm.get('location') if farm else 'Unspecified'
        area = f"{farm.get('area')} acres" if farm else 'Unspecified'
        soil_type = farm.get('soil_type') if farm else 'Unspecified'
        irrigation_method = farm.get('irrigation_method') if farm else 'Unspecified'
        
        crop_name = crop.get('name') if crop else 'No Active Crop'
        variety = crop.get('variety') if crop else 'Unspecified'
        planting_date = crop.get('planting_date') if crop else 'Unspecified'
        stage = crop.get('stage') if crop else 'Unspecified'
        
        specs_data = [
            [Paragraph("<b>Farm Name</b>", body_style), Paragraph(farm_name, body_style),
             Paragraph("<b>Active Crop</b>", body_style), Paragraph(crop_name, body_style)],
            [Paragraph("<b>Location</b>", body_style), Paragraph(location, body_style),
             Paragraph("<b>Crop Variety</b>", body_style), Paragraph(variety, body_style)],
            [Paragraph("<b>Area</b>", body_style), Paragraph(area, body_style),
             Paragraph("<b>Planting Date</b>", body_style), Paragraph(planting_date, body_style)],
            [Paragraph("<b>Soil Type</b>", body_style), Paragraph(soil_type, body_style),
             Paragraph("<b>Crop Stage</b>", body_style), Paragraph(stage, body_style)],
            [Paragraph("<b>Irrigation</b>", body_style), Paragraph(irrigation_method, body_style),
             Paragraph("", body_style), Paragraph("", body_style)]
        ]
        
        specs_table = Table(specs_data, colWidths=[100, 150, 100, 150])
        specs_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), bg_light),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2ECE2")),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('PADDING', (0,0), (-1,-1), 6),
        ]))
        story.append(specs_table)
        story.append(Spacer(1, 15))
        
        # 3. Latest Telemetry Readings
        story.append(Paragraph("2. Telemetry Parameters (Latest Observations)", h1_style))
        if observation:
            obs_data = [
                [Paragraph("<b>Parameter</b>", body_style), Paragraph("<b>Value</b>", body_style),
                 Paragraph("<b>Parameter</b>", body_style), Paragraph("<b>Value</b>", body_style)],
                [Paragraph("Soil Moisture", body_style), Paragraph(f"{observation.get('soil_moisture')}%", body_style),
                 Paragraph("Soil pH", body_style), Paragraph(f"{observation.get('soil_ph')}", body_style)],
                [Paragraph("Nitrogen (N)", body_style), Paragraph(f"{observation.get('nitrogen')} kg/ha", body_style),
                 Paragraph("Phosphorus (P)", body_style), Paragraph(f"{observation.get('phosphorus')} kg/ha", body_style)],
                [Paragraph("Potassium (K)", body_style), Paragraph(f"{observation.get('potassium')} kg/ha", body_style),
                 Paragraph("Rainfall", body_style), Paragraph(f"{observation.get('rainfall')} mm", body_style)],
                [Paragraph("Temperature", body_style), Paragraph(f"{observation.get('temperature')} °C", body_style),
                 Paragraph("Humidity", body_style), Paragraph(f"{observation.get('humidity')}%", body_style)],
                [Paragraph("Crop Health", body_style), Paragraph(f"{observation.get('crop_health')}%", body_style),
                 Paragraph("Mandi Price", body_style), Paragraph(f"INR {observation.get('market_price')}/q", body_style)]
            ]
        else:
            obs_data = [
                [Paragraph("No recent telemetry observations registered.", body_style)]
            ]
            
        obs_table = Table(obs_data, colWidths=[130, 120, 130, 120] if observation else [500])
        obs_table.setStyle(TableStyle([
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#DDDDDD")),
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#EEEEEE")) if observation else ('BACKGROUND', (0,0), (-1,-1), bg_light),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('PADDING', (0,0), (-1,-1), 5),
        ]))
        story.append(obs_table)
        story.append(Spacer(1, 15))

        # 4. Critical Warnings and Active Recommendations
        rec_elements = []
        rec_elements.append(Paragraph("3. Alerts & Priority Recommendations", h1_style))
        
        # Alerts
        if alerts:
            rec_elements.append(Paragraph("<b>Active Smart Alerts:</b>", body_style))
            for a in alerts[:3]:
                rec_elements.append(Paragraph(f"• [<b>{a.get('severity')}</b>] {a.get('title')}: {a.get('description')}", body_style))
            rec_elements.append(Spacer(1, 6))

        # Recommendations
        if recommendations:
            rec_elements.append(Paragraph("<b>Active Recommendations:</b>", body_style))
            for r in recommendations[:5]:
                rec_elements.append(Paragraph(f"• [<b>{r.get('priority')}</b>] {r.get('title')}: {r.get('description')} ({r.get('agent_name')})", body_style))
        else:
            rec_elements.append(Paragraph("No active recommendations listed.", body_style))
            
        story.append(KeepTogether(rec_elements))
        story.append(Spacer(1, 15))

        # 5. Farm Planning Coordinator Output
        plan_elements = []
        plan_elements.append(Paragraph("4. Synthesized Farm Plan & Reasoning", h1_style))
        
        if final_plan:
            # Parse final plan metrics
            overall_health = final_plan.get('overall_health', 'Good')
            overall_risk = final_plan.get('overall_risk', 'Low')
            confidence = final_plan.get('confidence', 'N/A')
            data_quality = final_plan.get('data_quality', 'N/A')
            summary = final_plan.get('summary', 'Plan generated successfully.')
            reasoning = final_plan.get('reasoning', '')

            plan_metrics = [
                [Paragraph("<b>Overall Farm Health</b>", body_style), Paragraph(str(overall_health), body_style),
                 Paragraph("<b>Plan Confidence</b>", body_style), Paragraph(f"{confidence}%" if '%' not in str(confidence) else str(confidence), body_style)],
                [Paragraph("<b>Overall Risk Level</b>", body_style), Paragraph(str(overall_risk), body_style),
                 Paragraph("<b>Data Quality Score</b>", body_style), Paragraph(f"{data_quality}%" if '%' not in str(data_quality) else str(data_quality), body_style)]
            ]
            
            plan_table = Table(plan_metrics, colWidths=[130, 120, 130, 120])
            plan_table.setStyle(TableStyle([
                ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2ECE2")),
                ('BACKGROUND', (0,0), (-1,-1), bg_light),
                ('PADDING', (0,0), (-1,-1), 5),
            ]))
            plan_elements.append(plan_table)
            plan_elements.append(Spacer(1, 8))
            
            plan_elements.append(Paragraph("<b>Plan Summary:</b>", body_style))
            plan_elements.append(Paragraph(summary, body_style))
            if reasoning:
                plan_elements.append(Paragraph("<b>Planning Reasoning:</b>", body_style))
                plan_elements.append(Paragraph(reasoning, body_style))
        else:
            plan_elements.append(Paragraph("No final plan has been generated. Execute the orchestrator on the dashboard to build an AI farm plan.", body_style))
            
        story.append(KeepTogether(plan_elements))
        
        # Build document
        doc.build(story)
        buffer.seek(0)
        return buffer
