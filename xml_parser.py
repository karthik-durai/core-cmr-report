import xml.etree.ElementTree as ET
import pandas as pd

def get_patient_info(patient):
    name = patient.find('Name').get('val')
    data_of_birth = patient.find('BirthDate').get('val')
    age = patient.find('Age').get('val')
    height = patient.find('Height').get('val')
    weight = patient.find('Weight').get('val')
    bsa = patient.find('Bsa').get('val')
    patient_id = patient.find('PatientID').get('val')
    return {
        'name': name, 'data_of_birth': data_of_birth, 'age': age, 'height': height, 'weight': weight, 'bsa': bsa, 'patient_id': patient_id
    }


def get_scanner_info(scan):
    scan_date = scan.find('StudyDate').get('val')
    institution_name = scan.find('InstitutionName').get('val')
    return {
        'scan_date': scan_date, 'institution_name': institution_name
    }

table_style = """
<style>
    table {
        width: 50%;
        border-collapse: collapse;
        margin: 20px 0;
        font-size: 18px;
        text-align: left;
    }
    th, td {
        border: 1px solid #ddd;
        padding: 8px;
    }
    th {
        background-color: #4CAF50;
        color: white;
    }
    tr:nth-child(even) {
        background-color: #f2f2f2;
    }
    td:empty {
        border-top: 1px solid #ddd;
        border-bottom: 1px solid #ddd;
        border-left: none;
        border-right: none;
        background: transparent;
    }
    .download-btn {
        display: block;
        width: 200px;
        padding: 10px;
        margin: 20px auto;
        text-align: center;
        background-color: #28a745;
        color: white;
        font-size: 16px;
        border: none;
        cursor: pointer;
        border-radius: 5px;
    }
</style>
"""

script = """
<script>
    function downloadPDF() {
        const { jsPDF } = window.jspdf;
        let doc = new jsPDF();
        doc.autoTable({ html: 'table' });
        doc.save("table.pdf");
    }
</script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf-autotable/3.5.28/jspdf.plugin.autotable.min.js"></script>
"""

def get_data(xml_data):
    document = ET.parse(xml_data)
    root = document.getroot()

    patient = root.find('Patient')
    scan = root.find('Study')

    patient_data = get_patient_info(patient)
    scan_data = get_scanner_info(scan)

    data = [
        ("Name:", patient_data['name'], "Date of Scan:", scan_data['scan_date']),
        ("Date of Birth:", patient_data['data_of_birth'], "Hospital Number:", scan_data['institution_name']),
        ("Height (cm):", patient_data['height'], "Weight (kg):", patient_data['weight']),
        ("BSA (m2):", patient_data['bsa'], "BMI (kg/m2):", ""),
        ("Referring Consultant:", "", "", ""),
        ("Patient History:", "", "", ""),
        ("Indication:", "", "", ""),
        ("Scanner type:", "", "Field strength (T):", ""),
        ("Sequences acquired:", "", "", ""),
        ("Contrast agent type:", "", "Contrast agent dose (mmol/kg):", ""),
    ]

    tabular_form_html = pd.DataFrame(data).to_html(header=None, index=False, escape=False)

    # HTML Content with Button
    html_content = f"""
    <html>
    <head>
        <title>Styled HTML Table</title>
        {table_style}
    </head>
    <body>
        <div>
            {tabular_form_html}
        </div>
        <button class="download-btn" onclick="downloadPDF()">Save as PDF</button>
        {script}
    </body>
    </html>
    """

    return html_content
