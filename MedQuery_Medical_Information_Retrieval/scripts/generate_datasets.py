"""
generate_datasets.py
Generates the comprehensive medical documents dataset (100+ educational documents)
and the evaluation queries dataset with ground-truth relevant document IDs.
Sources: Educational materials from WHO, CDC, NIH MedlinePlus, NHS, Mayo Clinic.
Disclaimer: This dataset is curated strictly for educational information retrieval research.
"""

import csv
import os

DOCUMENTS = [
    # 1. DIABETES
    {
        "document_id": "DOC_001",
        "title": "Type 2 Diabetes Mellitus: Overview, Etiology, and Management",
        "category": "Endocrinology",
        "disease": "Type 2 Diabetes",
        "symptoms": "Increased thirst (polydipsia), frequent urination (polyuria), unexplained weight loss, fatigue, blurred vision, slow-healing sores, frequent infections.",
        "causes": "Insulin resistance in peripheral tissues combined with progressive pancreatic beta-cell secretory defect. Risk factors include obesity, physical inactivity, genetics, and age over 45.",
        "treatment": "Lifestyle modifications (dietary changes, aerobic exercise), oral antihyperglycemic agents such as metformin, sulfonylureas, SGLT2 inhibitors, GLP-1 receptor agonists, and insulin therapy when indicated.",
        "prevention": "Maintaining a healthy body weight, engaging in at least 150 minutes of moderate physical activity weekly, consuming a balanced diet rich in whole grains and fiber, and regular screening.",
        "content": "Type 2 diabetes mellitus is a chronic metabolic disorder characterized by persistent hyperglycemia resulting from impaired insulin secretion and peripheral insulin resistance. Over time, poorly controlled type 2 diabetes leads to microvascular complications including diabetic retinopathy, nephropathy, and peripheral neuropathy, as well as macrovascular events such as myocardial infarction and stroke. Regular glycated hemoglobin (HbA1c) monitoring, blood pressure control, and lipid management are crucial pillars of clinical care. Patient education on self-monitoring of blood glucose and foot care prevents severe secondary morbidity.",
        "source": "NIH MedlinePlus & WHO Guidelines"
    },
    {
        "document_id": "DOC_002",
        "title": "Type 1 Diabetes Mellitus: Autoimmune Pathophysiology and Insulin Therapy",
        "category": "Endocrinology",
        "disease": "Type 1 Diabetes",
        "symptoms": "Rapid onset of excessive thirst, extreme hunger (polyphagia), frequent urination, bedwetting in children, unintended weight loss, extreme fatigue, irritability, sweet or fruity breath odor.",
        "causes": "Autoimmune destruction of pancreatic beta cells in the islets of Langerhans, mediated by T-cells. Triggered by genetic susceptibility combined with environmental triggers.",
        "treatment": "Lifelong exogenous insulin therapy via multiple daily injections or continuous subcutaneous insulin infusion (insulin pump), carbohydrate counting, continuous glucose monitoring (CGM).",
        "prevention": "Currently no established preventative measures exist for type 1 diabetes; clinical trials continue to investigate immune-modulating therapies for high-risk individuals with autoantibodies.",
        "content": "Type 1 diabetes mellitus is an autoimmune endocrine disorder typically presenting in childhood or early adulthood, although onset can occur at any age. The destruction of insulin-producing pancreatic beta cells leads to absolute insulin deficiency. Without exogenous insulin replacement, patients rapidly develop diabetic ketoacidosis (DKA), a life-threatening medical emergency marked by ketone accumulation, metabolic acidosis, and severe dehydration. Intensive insulin therapy matching insulin doses to carbohydrate intake and physical exertion is essential to maintain target glycemic levels and minimize hypoglycemia.",
        "source": "CDC & American Diabetes Association"
    },
    {
        "document_id": "DOC_003",
        "title": "Gestational Diabetes Mellitus: Maternal-Fetal Considerations and Screening",
        "category": "Endocrinology",
        "disease": "Gestational Diabetes",
        "symptoms": "Often asymptomatic; mild symptoms may include increased thirst, frequent urination, fatigue, and recurrent candidal infections.",
        "causes": "Placental hormones (human placental lactogen, cortisol, progesterone) inducing maternal peripheral insulin resistance beyond the compensatory capacity of maternal beta cells.",
        "treatment": "Nutritional counseling, medical nutrition therapy, daily blood glucose monitoring, moderate physical activity, and pharmacological therapy (insulin or metformin) if targets are unmet.",
        "prevention": "Achieving a healthy body mass index before conception, regular physical exercise before and during pregnancy, and adhering to nutrient-dense dietary guidelines.",
        "content": "Gestational diabetes mellitus (GDM) is defined as glucose intolerance with onset or first recognition during pregnancy, typically evaluated between 24 and 28 weeks of gestation using oral glucose tolerance testing (OGTT). Uncontrolled maternal hyperglycemia increases the risk of macrosomia, birth trauma, neonatal hypoglycemia, respiratory distress syndrome, and preeclampsia. Postpartum follow-up is essential as women with gestational diabetes have a significantly elevated lifetime risk of developing chronic type 2 diabetes mellitus.",
        "source": "WHO Guidelines & Mayo Clinic"
    },
    {
        "document_id": "DOC_004",
        "title": "Diabetic Ketoacidosis: Recognition, Biochemical Mechanisms, and Emergency Protocol",
        "category": "Endocrinology",
        "disease": "Diabetic Ketoacidosis",
        "symptoms": "Deep rapid breathing (Kussmaul respiration), acetone fruity breath odor, nausea, severe vomiting, abdominal pain, extreme dehydration, confusion, lethargy, stupor.",
        "causes": "Profound insulin deficiency coupled with counter-regulatory hormone excess (glucagon, catecholamines, cortisol), precipitating lipolysis and hepatic ketogenesis. Common triggers include infection, missed insulin doses, or newly diagnosed diabetes.",
        "treatment": "Aggressive intravenous fluid resuscitation with isotonic saline, continuous low-dose intravenous regular insulin infusion, potassium repletion, and correction of electrolyte derangements.",
        "prevention": "Consistent adherence to insulin regimens, adherence to sick-day management rules (frequent blood glucose and urinary/blood ketone checks), and prompt treatment of intercurrent infections.",
        "content": "Diabetic ketoacidosis (DKA) is an acute, critical metabolic complication seen primarily in type 1 diabetes but also occurring in type 2 diabetes during severe physiologic stress. Lack of insulin prevents cellular glucose utilization, driving the breakdown of adipose tissue into free fatty acids which are converted by the liver into acidic ketone bodies (acetoacetate, beta-hydroxybutyrate). This produces severe anion-gap metabolic acidosis and osmotic diuresis leading to profound fluid and electrolyte depletion requiring intensive hemodynamic monitoring.",
        "source": "NIH MedlinePlus & Endocrine Society"
    },
    {
        "document_id": "DOC_005",
        "title": "Hypoglycemia in Diabetic Patients: Pathophysiology and Emergency Action",
        "category": "Endocrinology",
        "disease": "Hypoglycemia",
        "symptoms": "Tremors, tachycardia, diaphoresis, pallor, intense hunger, anxiety, dizziness, confusion, slurred speech, visual disturbances, seizures, loss of consciousness.",
        "causes": "Excessive exogenous insulin administration, skipped or delayed meals, unanticipated strenuous physical exercise, alcohol consumption, or renal impairment.",
        "treatment": "Immediate ingestion of 15-20 grams of fast-acting simple carbohydrates (rule of 15: glucose tablets, fruit juice); intramuscular or nasal glucagon administration for unconscious patients; intravenous dextrose 50% in acute hospital settings.",
        "prevention": "Frequent glycemic monitoring, adjusting insulin dosages during exercise, carrying portable glucose sources at all times, wearing medical identification jewelry, and diabetes self-management training.",
        "content": "Hypoglycemia is defined clinically as a plasma glucose concentration below 70 mg/dL (3.9 mmol/L). It triggers autonomic activation resulting in neurogenic symptoms (shakiness, diaphoresis, palpitations) followed by neuroglycopenic manifestations (cognitive impairment, confusion, syncope) as cerebral glucose deprivation ensues. Severe hypoglycemia is a medical emergency that can precipitate cardiac arrhythmias, irreversible neurological injury, or death if not promptly reversed.",
        "source": "CDC & Mayo Clinic"
    },

    # 2. HYPERTENSION & CARDIOVASCULAR
    {
        "document_id": "DOC_006",
        "title": "Essential Primary Hypertension: Pathogenesis and Clinical Guidelines",
        "category": "Cardiovascular",
        "disease": "Primary Hypertension",
        "symptoms": "Often termed the 'silent killer' due to absence of overt symptoms; severe elevations may present with occipital morning headache, dizziness, epistaxis, tinnitus, and exertional dyspnea.",
        "causes": "Multifactorial etiology involving genetic predisposition, high dietary sodium intake, low potassium intake, endothelial dysfunction, renin-angiotensin-aldosterone system (RAAS) overactivity, and chronic sympathetic activation.",
        "treatment": "Lifestyle interventions (DASH diet, sodium restriction <2g/day, weight loss, exercise), first-line pharmacotherapy with ACE inhibitors, ARBs, thiazide diuretics, or dihydropyridine calcium channel blockers.",
        "prevention": "Adopting the DASH eating plan, maintaining healthy body mass index, smoking cessation, limiting alcohol consumption, regular physical exercise, and stress reduction techniques.",
        "content": "Essential hypertension accounts for over 90% of all clinical hypertension cases and is diagnosed when systolic blood pressure is persistently >=130 mmHg or diastolic blood pressure >=80 mmHg. Chronic sustained hemodynamic strain accelerates atherosclerosis and causes left ventricular hypertrophy, hypertensive nephrosclerosis, ischemic heart disease, and cerebrovascular accidents. Routine ambulatory blood pressure monitoring and patient adherence to long-term antihypertensive therapy are crucial to prevent irreversible target-organ damage.",
        "source": "American Heart Association & WHO Guidelines"
    },
    {
        "document_id": "DOC_007",
        "title": "Secondary Hypertension: Identifiable Causes and Diagnostic Workup",
        "category": "Cardiovascular",
        "disease": "Secondary Hypertension",
        "symptoms": "Refractory hypertension resistant to multi-drug therapy, sudden onset before age 30 or after 55, episodic sweating with palpitations (pheochromocytoma), daytime somnolence and loud snoring (sleep apnea).",
        "causes": "Renal artery stenosis (renovascular disease), chronic kidney disease, primary hyperaldosteronism (Conn syndrome), obstructive sleep apnea, Cushing syndrome, pheochromocytoma, aortic coarctation, or medications (NSAIDs, oral contraceptives).",
        "treatment": "Targeted treatment of the underlying etiology: renal angioplasty, adrenalectomy for functional tumors, CPAP for sleep apnea, surgical repair of coarctation, or discontinuing offending pharmacological agents.",
        "prevention": "Early detection and management of underlying endocrine, vascular, and renal disorders; periodic medication review to eliminate secondary hypertensive triggers.",
        "content": "Secondary hypertension represents approximately 5-10% of adult hypertension cases where an identifiable, potentially curable cause exists. Suspecting secondary hypertension is indicated in patients with resistant hypertension (uncontrolled on three concurrent antihypertensives including a diuretic), severe sudden blood pressure surges, or abnormal clinical signs such as abdominal bruits or severe hypokalemia. Comprehensive diagnostic evaluation includes renal duplex ultrasonography, plasma renin-to-aldosterone ratio, overnight polysomnography, and plasma metanephrines.",
        "source": "NIH MedlinePlus & European Society of Cardiology"
    },
    {
        "document_id": "DOC_008",
        "title": "Hypertensive Crisis: Hypertensive Urgency versus Hypertensive Emergency",
        "category": "Cardiovascular",
        "disease": "Hypertensive Crisis",
        "symptoms": "Severe headache, chest pain, dyspnea, visual blurriness, neurological deficits, back pain (aortic dissection), vomiting, altered mental status, seizures.",
        "causes": "Abrupt escalation of systemic vascular resistance often due to non-adherence to chronic antihypertensive regimens, acute renal disease, cocaine or amphetamine toxicity, or preeclampsia/eclampsia.",
        "treatment": "For hypertensive emergency (with target organ damage): immediate ICU admission and parenteral titratable antihypertensives (labetalol, nicardipine, nitroprusside) aiming for controlled gradual reduction. For urgency: oral medications in outpatient setting.",
        "prevention": "Strict adherence to daily antihypertensive prescriptions, routine blood pressure self-monitoring, avoiding illicit sympathomimetic drugs, and prompt outpatient medical consultation upon detecting elevated readings.",
        "content": "A hypertensive crisis is characterized by a severe elevation in blood pressure, typically systolic >180 mmHg and/or diastolic >120 mmHg. It is classified into two distinct clinical categories: hypertensive emergency, which involves acute, life-threatening target-organ damage (acute coronary syndrome, encephalopathy, aortic dissection, acute renal failure, pulmonary edema), versus hypertensive urgency, where blood pressure is markedly elevated without acute organ impairment. Rapid uncontrolled lowering in urgency is contraindicated to avoid cerebral hypoperfusion.",
        "source": "American Heart Association & NIH MedlinePlus"
    },
    {
        "document_id": "DOC_009",
        "title": "Coronary Artery Disease: Atherosclerotic Plaque and Myocardial Ischemia",
        "category": "Cardiovascular",
        "disease": "Coronary Artery Disease",
        "symptoms": "Substernal chest pressure or squeezing (angina pectoris), radiation of pain to left arm, neck, or jaw, exertional dyspnea, diaphoresis, nausea, weakness, fatigue.",
        "causes": "Atherosclerotic plaque accumulation within coronary arteries reducing myocardial perfusion. Risk factors include dyslipidemia, smoking, hypertension, diabetes mellitus, sedentary lifestyle, and obesity.",
        "treatment": "Antiplatelet therapy (aspirin, P2Y12 inhibitors), high-intensity statins, beta-blockers, ACE inhibitors, sublingual nitroglycerin, revascularization via percutaneous coronary intervention (PCI/stent) or CABG surgery.",
        "prevention": "Smoking cessation, Mediterranean-style diet, achieving LDL cholesterol targets, regular aerobic cardiovascular exercise, blood pressure control, and tight glycemic regulation in diabetics.",
        "content": "Coronary artery disease (CAD) develops as fibrofatty plaques progressively narrow coronary arterial lumens, limiting oxygen delivery to the myocardium during heightened metabolic demand. Stable angina manifests as predictable exertional pain relieved by rest or nitroglycerin. Plaque rupture or erosion triggers acute platelet aggregation and thrombus formation, culminating in acute coronary syndromes (unstable angina or myocardial infarction). Coronary computed tomography angiography and invasive cardiac catheterization serve as gold-standard diagnostic tools.",
        "source": "NIH MedlinePlus & Mayo Clinic"
    },
    {
        "document_id": "DOC_010",
        "title": "Congestive Heart Failure: Systolic and Diastolic Ventricular Dysfunction",
        "category": "Cardiovascular",
        "disease": "Heart Failure",
        "symptoms": "Exertional dyspnea, orthopnea (shortness of breath lying flat), paroxysmal nocturnal dyspnea, bilateral lower extremity peripheral edema, jugular venous distention, fatigue, persistent cough with pink frothy sputum.",
        "causes": "Ischemic heart disease, chronic long-standing hypertension, dilated or hypertrophic cardiomyopathy, valvular heart disease, myocarditis, cardiac arrhythmias, and cardiotoxic chemotherapies.",
        "treatment": "Guideline-directed medical therapy (GDMT): ARNI (sacubitril/valsartan) or ACEi/ARB, evidence-based beta-blockers (carvedilol, metoprolol succinate), mineralocorticoid receptor antagonists (spironolactone), SGLT2 inhibitors, loop diuretics (furosemide) for decongestion.",
        "prevention": "Aggressive management of hypertension, early revascularization in ischemic heart disease, moderation of alcohol intake, weight management, and prevention of coronary atherosclerosis.",
        "content": "Congestive heart failure (CHF) is a complex clinical syndrome resulting from structural or functional cardiac impairment that prevents the ventricles from filling or ejecting blood effectively. It is categorized into heart failure with reduced ejection fraction (HFrEF) and heart failure with preserved ejection fraction (HFpEF). Elevated intracardiac filling pressures result in pulmonary congestion and systemic venous hypertension. Serum B-type natriuretic peptide (BNP) or NT-proBNP measurement combined with transthoracic echocardiography is foundational for diagnosis and therapeutic staging.",
        "source": "American College of Cardiology & NHS"
    },

    # 3. RESPIRATORY CONDITIONS
    {
        "document_id": "DOC_011",
        "title": "Bronchial Asthma: Airway Hyperresponsiveness and Chronic Inflammation",
        "category": "Respiratory",
        "disease": "Asthma",
        "symptoms": "Recurrent wheezing, episodic shortness of breath, chest tightness, nocturnal or early-morning dry cough, exertional respiratory distress.",
        "causes": "Complex gene-environment interactions leading to chronic airway eosinophilic or neutrophilic inflammation. Common triggers include airborne allergens (dust mites, pollen, pet dander), viral respiratory infections, cold dry air, tobacco smoke, and exercise.",
        "treatment": "Inhaled corticosteroids (ICS) as cornerstone controller therapy, combined with long-acting beta2-agonists (LABA); short-acting beta2-agonists (albuterol) for rescue bronchodilation; leukotriene receptor antagonists; biologic therapies (anti-IgE, anti-IL5) in refractory disease.",
        "prevention": "Identifying and avoiding specific environmental allergens and irritants, annual influenza and pneumococcal immunizations, maintaining smoke-free living quarters, and following an individualized written asthma action plan.",
        "content": "Bronchial asthma is a heterogeneous chronic inflammatory respiratory disease characterized by reversible bronchoconstriction, bronchial wall edema, and mucus hypersecretion. Spirometry demonstrates airflow limitation with significant reversibility following inhaled bronchodilator administration (increase in FEV1 >=12% and >=200 mL). Asthma phenotypes include allergic (atopic) asthma, non-allergic asthma, adult-onset asthma, and exercise-induced bronchoconstriction. Proper inhaler technique and adherence to daily anti-inflammatory controller therapy are essential to prevent severe exacerbations and airway remodeling.",
        "source": "Global Initiative for Asthma (GINA) & NIH MedlinePlus"
    },
    {
        "document_id": "DOC_012",
        "title": "Exercise-Induced Bronchoconstriction: Mechanism and Management in Athletes",
        "category": "Respiratory",
        "disease": "Exercise-Induced Asthma",
        "symptoms": "Coughing, wheezing, chest tightness, and shortness of breath occurring during or typically 5 to 15 minutes following vigorous physical exertion.",
        "causes": "Rapid ventilation during exercise leads to hyperosmolarity of the airway surface liquid due to thermal and water loss, triggering mast cell degranulation and release of histamine and leukotrienes.",
        "treatment": "Pre-treatment with short-acting beta2-agonists (SABA) 10-15 minutes prior to exercise; daily inhaled corticosteroids (ICS) or leukotriene receptor antagonists (montelukast) for frequent exercise or uncontrolled symptoms.",
        "prevention": "Thorough warm-up routine before high-intensity activity, breathing through the nose rather than the mouth, wearing a heat-exchange mask in freezing weather, and avoiding workouts in heavily polluted or pollen-dense environments.",
        "content": "Exercise-induced bronchoconstriction (EIB) involves transient airway narrowing triggered by physical exertion. While frequently occurring in individuals with established chronic asthma, it also arises in elite athletes without baseline asthma symptoms, particularly in cold-weather sports (cross-country skiing, ice hockey) and swimming (due to chlorine derivatives). Diagnosis is confirmed through standardized exercise challenge testing or eucapnic voluntary hyperpnea. With appropriate pre-exercise pharmacotherapy, affected individuals can safely participate in all physical and competitive sporting activities.",
        "source": "Mayo Clinic & American Thoracic Society"
    },
    {
        "document_id": "DOC_013",
        "title": "Community-Acquired Pneumonia: Etiology, Clinical Presentation, and Antibiotic Regimens",
        "category": "Respiratory",
        "disease": "Pneumonia",
        "symptoms": "High fever, chills, rigors, productive cough with purulent or rust-colored sputum, pleuritic chest pain, dyspnea, tachypnea, crackles/rales on lung auscultation, confusion in elderly patients.",
        "causes": "Bacterial pathogens (Streptococcus pneumoniae, Haemophilus influenzae, atypical pathogens: Mycoplasma pneumoniae, Legionella pneumophila), viral pathogens (influenza, RSV, SARS-CoV-2), and occasionally fungi.",
        "treatment": "Empiric antimicrobial therapy based on clinical severity (CURB-65 score): outpatient macrolides, doxycycline, or amoxicillin/clavulanate; inpatient respiratory fluoroquinolones or beta-lactam plus macrolide; supplemental oxygen and intravenous hydration.",
        "prevention": "Pneumococcal vaccination (PCV15/PCV20, PPSV23), annual influenza immunization, tobacco cessation, good hand hygiene, and aspiration prevention in vulnerable individuals.",
        "content": "Community-acquired pneumonia (CAP) is an acute infection of the lung parenchyma characterized by alveolar exudative consolidation. Chest radiography demonstrating new pulmonary infiltrates is required to establish diagnosis. The inflammatory response leads to ventilation-perfusion mismatch and hypoxemia. Elderly patients may present atypically without marked fever, manifesting instead with altered mental status, functional decline, or decompensation of comorbid heart failure. Stratification tools such as CURB-65 and the Pneumonia Severity Index guide safe outpatient versus inpatient admission decisions.",
        "source": "CDC & American Thoracic Society"
    },
    {
        "document_id": "DOC_014",
        "title": "Aspiration Pneumonia: Risk Factors, Anaerobic Flora, and Clinical Care",
        "category": "Respiratory",
        "disease": "Aspiration Pneumonia",
        "symptoms": "Subacute onset of fever, cough with foul-smelling sputum, dyspnea, hypoxemia, weight loss, crackles localized to dependent pulmonary segments.",
        "causes": "Inhalation of colonized oropharyngeal or gastric secretions into the lower respiratory tract, caused by impaired swallowing (dysphagia), altered consciousness (alcoholism, anesthesia, stroke), gastroesophageal reflux, or enteral tube feeding.",
        "treatment": "Antimicrobial coverage targeting oral anaerobes and gram-negative bacilli (ampicillin-sulbactam, piperacillin-tazobactam, or clindamycin), respiratory support, and speech-language therapy for swallowing rehabilitation.",
        "prevention": "Elevation of head of bed to 30-45 degrees during and after meals, texture-modified diets (thickened liquids, pureed foods), meticulous oral hygiene, and avoiding heavy sedatives.",
        "content": "Aspiration pneumonia develops when chemical irritation or microbial invasion occurs secondary to aspirated foreign material. It predominantly involves the dependent segments of the lungs: posterior segments of the upper lobes when recumbent, or superior segments of the lower lobes. Chemical pneumonitis (Mendelson syndrome) represents non-infectious inflammatory response to acid aspiration, whereas bacterial aspiration pneumonia requires targeted antimicrobial therapy. Formal videofluoroscopic swallowing study helps evaluate aspiration risk and guide feeding strategies.",
        "source": "NIH MedlinePlus & European Respiratory Journal"
    },
    {
        "document_id": "DOC_015",
        "title": "Chronic Obstructive Pulmonary Disease: Emphysema, Chronic Bronchitis, and Bronchodilators",
        "category": "Respiratory",
        "disease": "COPD",
        "symptoms": "Progressive exertional dyspnea, chronic productive cough with white or clear sputum, frequent chest infections, wheezing, barrel chest, pursed-lip breathing, peripheral cyanosis.",
        "causes": "Long-term inhalation of noxious particles and gases, predominantly cigarette smoke; occupational biomass smoke, coal dust, chemical vapors; and genetic alpha-1 antitrypsin deficiency.",
        "treatment": "Long-acting muscarinic antagonists (LAMA) and long-acting beta2-agonists (LABA), inhaled corticosteroids for high exacerbation phenotypes, pulmonary rehabilitation, supplemental oxygen for resting hypoxemia.",
        "prevention": "Primary prevention is strict avoidance or cessation of tobacco smoking, reducing occupational dust exposure, adequate indoor ventilation, and timely immunizations against pneumococcus, influenza, and RSV.",
        "content": "Chronic Obstructive Pulmonary Disease (COPD) is a progressive, partially reversible obstructive lung disease encompassing chronic bronchitis (mucus hypersecretion with productive cough for >=3 months in 2 consecutive years) and emphysema (destruction of alveolar walls and loss of pulmonary elastic recoil). Diagnosis is confirmed by post-bronchodilator spirometry demonstrating FEV1/FVC < 0.70. Airway collapse on expiration leads to gas trapping and hyperinflation. Comprehensive pulmonary rehabilitation markedly improves functional exercise capacity and quality of life.",
        "source": "Global Initiative for Chronic Obstructive Lung Disease (GOLD) & WHO"
    },

    # 4. INFECTIOUS DISEASES (VIRAL & BACTERIAL)
    {
        "document_id": "DOC_016",
        "title": "The Common Cold: Rhinovirus Pathogenesis and Symptomatic Relief",
        "category": "Infectious Diseases",
        "disease": "Common Cold",
        "symptoms": "Rhinorrhea (clear or mucopurulent nasal discharge), nasal congestion, sneezing, sore throat, mild low-grade fever, malaise, mild dry cough, mild headache.",
        "causes": "Over 200 viral strains, with Rhinoviruses causing over 50% of cases; other agents include coronaviruses (seasonal), adenoviruses, enteroviruses, and respiratory syncytial virus (RSV).",
        "treatment": "Symptomatic and supportive therapy: oral hydration, saline nasal irrigation, topical or oral decongestants (pseudoephedrine, short-term oxymetazoline), analgesics/antipyretics (acetaminophen, ibuprofen). Antibiotics are completely ineffective and inappropriate.",
        "prevention": "Frequent handwashing with soap and water, avoiding touching the eyes, nose, and mouth, disinfecting frequently touched surfaces, and minimizing close contact with infected individuals.",
        "content": "The common cold is a self-limiting acute viral upper respiratory tract infection. Transmission occurs primarily through respiratory droplets and direct contact with fomites. Viral attachment to ICAM-1 receptors on nasopharyngeal epithelial cells triggers host chemokine release, leading to vasodilatation, increased vascular permeability, and glandular secretion. Symptoms typically peak within 2 to 3 days and resolve spontaneously within 7 to 10 days. Routine antibiotic administration is contraindicated as it confers no therapeutic benefit and drives antimicrobial resistance.",
        "source": "CDC & NIH MedlinePlus"
    },
    {
        "document_id": "DOC_017",
        "title": "Seasonal Influenza: Clinical Distinction, Influenza A/B, and Antiviral Neuraminidase Inhibitors",
        "category": "Infectious Diseases",
        "disease": "Influenza",
        "symptoms": "Abrupt onset of high fever (101-104°F), rigors, severe myalgia and arthralgia, profound physical fatigue, prostration, severe headache, dry non-productive cough, sore throat.",
        "causes": "Influenza A and B orthomyxoviruses with antigenic surface glycoproteins hemagglutinin (HA) and neuraminidase (NA), transmitted via aerosolized respiratory droplets.",
        "treatment": "Oral neuraminidase inhibitors (oseltamivir) or cap-dependent endonuclease inhibitor (baloxavir marboxil) initiated within 48 hours of symptom onset; supportive antipyretics, adequate oral fluid intake, and bed rest.",
        "prevention": "Annual quadrivalent influenza vaccination, respiratory hygiene and cough etiquette, early antiviral post-exposure chemoprophylaxis in high-risk institutional settings.",
        "content": "Influenza is an acute respiratory infection characterized by systemic toxicity and rapid onset of debilitating symptoms distinguishing it from the common cold. Antigenic drift causes continuous minor mutations in surface glycoproteins, necessitating annual reformulation of influenza vaccines. Complications include secondary bacterial pneumonia (commonly caused by Streptococcus pneumoniae or Staphylococcus aureus), myositis, myocarditis, and exacerbation of underlying asthma or congestive heart failure. Early antiviral therapy shortens illness duration and decreases severe complications in hospitalized and high-risk patients.",
        "source": "CDC & WHO Guidelines"
    },
    {
        "document_id": "DOC_018",
        "title": "Dengue Fever: Vector Biology, Phase Progression, and Warning Signs",
        "category": "Infectious Diseases",
        "disease": "Dengue",
        "symptoms": "Sudden high biphasic fever (up to 104°F), retro-orbital eye pain, severe frontal headache, intense muscular and bone aches ('breakbone fever'), nausea, maculopapular rash, mild petechiae.",
        "causes": "Dengue virus (DENV-1, DENV-2, DENV-3, DENV-4), a single-stranded RNA flavivirus transmitted through the bites of infective female Aedes mosquitoes (Aedes aegypti and Aedes albopictus).",
        "treatment": "Supportive management with meticulous oral and intravenous isotonic fluid replacement, paracetamol (acetaminophen) for analgesia and fever. Avoid NSAIDs (aspirin, ibuprofen) due to heightened hemorrhage risk.",
        "prevention": "Mosquito vector control (eliminating standing water containers, larvicidal application), utilizing insect repellents containing DEET, window screens, insecticide-treated bed nets, and dengue vaccination in endemic areas for seropositive individuals.",
        "content": "Dengue fever is a major mosquito-borne tropical viral disease. The clinical course transitions through three distinct phases: febrile, critical, and recovery. The critical phase occurs around days 3 to 7 as fever breaks, during which systemic capillary leakage can suddenly develop. Clinical warning signs—persistent vomiting, severe abdominal pain, mucosal bleeding, lethargy, fluid accumulation (ascites, pleural effusion), and rapid platelet drop with rising hematocrit—herald severe dengue (dengue hemorrhagic fever) and necessitate urgent inpatient fluid resuscitation.",
        "source": "WHO Guidelines & CDC"
    },
    {
        "document_id": "DOC_019",
        "title": "Severe Dengue and Dengue Shock Syndrome: Hemodynamic Collapse and Management",
        "category": "Infectious Diseases",
        "disease": "Severe Dengue",
        "symptoms": "Profound hypotension, narrow pulse pressure (<=20 mmHg), cold clammy skin, profound restlessness, rapid weak thready pulse, massive mucosal or gastrointestinal hemorrhage, hepatomegaly.",
        "causes": "Antibody-dependent enhancement (ADE) following secondary infection with a heterologous dengue viral serotype, precipitating hyperinflammatory cytokine storm and acute plasma leakage.",
        "treatment": "Immediate emergency resuscitation with crystalloid intravenous fluids (e.g., Ringer's lactate or normal saline) titrated against hematocrit and urine output; colloids or blood component transfusions in refractory shock or severe hemorrhage.",
        "prevention": "Community-wide integrated mosquito vector management, personal protective mosquito measures, and avoiding re-exposure in high-transmission zones.",
        "content": "Dengue Shock Syndrome (DSS) represents the most severe manifestation of dengue viral infection, resulting from widespread endothelial dysfunction and massive vascular plasma extravasation. Secondary dengue infections with a different serotype are particularly prone to ADE, wherein non-neutralizing antibodies facilitate viral entry into mononuclear cells, amplifying viral replication and inflammatory cytokine release. Timely, protocolized fluid titration guided by serial hematocrit measurements is life-saving, preventing both irreversible hypovolemic shock and iatrogenic fluid overload.",
        "source": "WHO & Pan American Health Organization"
    },
    {
        "document_id": "DOC_020",
        "title": "Malaria: Plasmodium Life Cycle, Diagnostic Microscopy, and Artemisinin Combination Therapy",
        "category": "Infectious Diseases",
        "disease": "Malaria",
        "symptoms": "Paroxysms of shivering chills (cold stage), high spiking fever (hot stage), profuse sweating (sweating stage), headache, fatigue, hemolytic anemia, splenomegaly, jaundice.",
        "causes": "Parasitic protozoa of the genus Plasmodium (P. falciparum, P. vivax, P. malariae, P. ovale, P. knowlesi), transmitted through the bite of infected female Anopheles mosquitoes.",
        "treatment": "Artemisinin-based combination therapies (ACTs: artemether-lumefantrine, artesunate-amodiaquine) for uncomplicated P. falciparum; intravenous artesunate for severe complicated malaria; primaquine to eradicate hypnozoites in P. vivax and P. ovale.",
        "prevention": "Sleeping under insecticide-treated mosquito nets (ITNs), indoor residual spraying, chemoprophylaxis (atovaquone-proguanil, doxycycline, mefloquine) for travelers, and RTS,S/AS01 or R21 malaria vaccines in high-risk pediatric populations.",
        "content": "Malaria is a life-threatening protozoal infection endemic in tropical and subtropical regions. Inoculated sporozoites invade hepatocytes before releasing merozoites that infect erythrocytes, leading to cyclical erythrocyte rupture responsible for clinical paroxysms. P. falciparum is the most virulent species, causing microvascular cytoadherence and sequestration that can result in cerebral malaria, acute respiratory distress, severe hemolytic anemia, and multi-organ failure. Confirmation via microscopic examination of thick and thin blood smears or rapid diagnostic antigen tests (RDTs) is essential prior to therapy.",
        "source": "WHO Guidelines & CDC"
    },
    {
        "document_id": "DOC_021",
        "title": "Cerebral Malaria: Neuropathology, Seizures, and Intensive Care Protocol",
        "category": "Infectious Diseases",
        "disease": "Cerebral Malaria",
        "symptoms": "Unarousable coma lasting >1 hour after generalized seizure, decerebrate or decorticate posturing, conjugate gaze deviation, retinal hemorrhages, severe metabolic acidosis, hyperpyrexia.",
        "causes": "Sequestration of parasitized erythrocytes expressing Plasmodium falciparum erythrocyte membrane protein 1 (PfEMP1) within cerebral capillaries, causing microvascular occlusion, tissue hypoxia, and blood-brain barrier breakdown.",
        "treatment": "Intravenous artesunate administered immediately at 0, 12, and 24 hours, followed by daily doses; careful fluid management to prevent cerebral or pulmonary edema; anticonvulsants (fosphenytoin) for status epilepticus.",
        "prevention": "Early diagnosis and prompt treatment of uncomplicated falciparum malaria; chemoprophylaxis and bite prevention in malaria-endemic zones.",
        "content": "Cerebral malaria is the most lethal neurological complication of Plasmodium falciparum malaria, primarily affecting young children in sub-Saharan Africa and non-immune adults in endemic zones. Cytoadherence of mature trophozoites and schizonts to endothelial receptors (ICAM-1, EPCR) induces endothelial inflammation and focal ischemia without typical inflammatory meningitis. Mortality remains high (15-20%) even with optimal antimalarial therapy. Survivors may experience persistent neurocognitive deficits, ataxia, blindness, or secondary epilepsy.",
        "source": "WHO Guidelines & The Lancet Infectious Diseases"
    },
    {
        "document_id": "DOC_022",
        "title": "Pulmonary Tuberculosis: Mycobacterium tuberculosis Transmission and DOTS Strategy",
        "category": "Infectious Diseases",
        "disease": "Tuberculosis",
        "symptoms": "Persistent cough lasting >3 weeks, hemoptysis (coughing up blood), low-grade evening fever, night sweats, unexplained weight loss ('consumption'), anorexia, chest pain.",
        "causes": "Infection by the acid-fast bacillus Mycobacterium tuberculosis, transmitted via airborne droplet nuclei generated when an infected person coughs, sneezes, or speaks.",
        "treatment": "Standard 6-month quadruple antimicrobial regimen under Directly Observed Therapy Short-course (DOTS): 2 months of intensive RHEZ (Rifampicin, Isoniazid, Pyrazinamide, Ethambutol) followed by 4 months of continuation phase (Rifampicin, Isoniazid).",
        "prevention": "BCG (Bacille Calmette-Guérin) vaccination at birth in endemic countries, airborne infection isolation rooms (negative pressure) in healthcare facilities, screening of close household contacts, and treatment of latent TB.",
        "content": "Tuberculosis (TB) remains one of the world's deadliest infectious killers. Inhaled mycobacteria are engulfed by alveolar macrophages, initiating granuloma (tubercle) formation with caseous necrosis. In immunocompetent hosts, cell-mediated immunity contains the bacilli in a latent state; however, immunosuppression (especially HIV infection, malnutrition, or anti-TNF therapy) permits reactivation into active pulmonary disease. Diagnosis is confirmed by sputum smear microscopy for acid-fast bacilli, rapid molecular assays (GeneXpert MTB/RIF), and mycobacterial liquid culture.",
        "source": "WHO Global TB Report & CDC"
    },
    {
        "document_id": "DOC_023",
        "title": "Multidrug-Resistant Tuberculosis (MDR-TB): Molecular Detection and Second-Line Regimens",
        "category": "Infectious Diseases",
        "disease": "Drug-Resistant Tuberculosis",
        "symptoms": "Similar to drug-susceptible TB (chronic productive cough, hemoptysis, fever, severe wasting, fatigue) but failing to resolve on standard first-line antitubercular therapy.",
        "causes": "Mycobacterium tuberculosis strains possessing chromosomal mutations conferring resistance to at least isoniazid and rifampicin, caused by inconsistent medication supply, incomplete adherence, or primary transmission of resistant strains.",
        "treatment": "Second-line antitubercular regimens incorporating bedaquiline, pretomanid, linezolid, and fluoroquinolones (moxifloxacin or levofloxacin), administered for 6 to 18 months depending on resistance profile.",
        "prevention": "Ensuring 100% completion of first-line DOTS regimens, rapid molecular drug-susceptibility testing (GeneXpert) for all diagnosed TB cases, and strict infection control in TB clinics.",
        "content": "Multidrug-resistant tuberculosis (MDR-TB) is a grave public health crisis that threatens global tuberculosis eradication. Resistance to rifampicin and isoniazid necessitates prolonged, more toxic, and considerably more expensive treatment regimens. Recent World Health Organization guidelines endorse all-oral, shorter novel regimens (such as BPaL/BPaLM: bedaquiline, pretomanid, linezolid, with or without moxifloxacin) that demonstrate superior cure rates and reduced adverse effects compared to older injectable-based regimens.",
        "source": "WHO Guidelines & New England Journal of Medicine"
    },
    {
        "document_id": "DOC_024",
        "title": "COVID-19 Acute Respiratory Infection: SARS-CoV-2 Pathogenesis, Variants, and Antivirals",
        "category": "Infectious Diseases",
        "disease": "COVID-19",
        "symptoms": "Fever, dry cough, dyspnea, fatigue, anosmia (loss of smell), ageusia (loss of taste), sore throat, congestion, myalgia, diarrhea; severe cases progress to hypoxemic respiratory failure.",
        "causes": "Infection with Severe Acute Respiratory Syndrome Coronavirus 2 (SARS-CoV-2), an enveloped positive-sense single-stranded RNA virus entering host cells via the ACE2 receptor.",
        "treatment": "Oral antivirals (nirmatrelvir-ritonavir [Paxlovid], remdesivir) initiated early; systemic corticosteroids (dexamethasone) and IL-6 inhibitors (tocilizumab) or baricitinib in hypoxemic hospitalized patients requiring oxygen.",
        "prevention": "mRNA and protein subunit vaccination, bivalent booster doses, high-filtration masks (N95/KN95) in crowded spaces, improved ventilation, and prompt testing upon symptom emergence.",
        "content": "Coronavirus disease 2019 (COVID-19) is a viral illness that emerged in late 2019 and precipitated a global pandemic. While many cases are mild or moderate, severe manifestations include viral pneumonia, acute respiratory distress syndrome (ARDS), hypercoagulability leading to pulmonary embolism or stroke, and dysregulated hyperinflammatory cytokine responses. Point-of-care rapid antigen testing and laboratory reverse-transcription polymerase chain reaction (RT-PCR) are standard diagnostic modalities. Monoclonal antibodies and antiviral agents have evolved alongside emerging variant strains (Alpha, Delta, Omicron sub-lineages).",
        "source": "CDC & NIH COVID-19 Treatment Guidelines"
    },
    {
        "document_id": "DOC_025",
        "title": "Post-Acute Sequelae of COVID-19 (Long COVID): Multi-System Manifestations",
        "category": "Infectious Diseases",
        "disease": "Long COVID",
        "symptoms": "Profound post-exertional malaise (PEM), cognitive impairment ('brain fog'), chronic fatigue, dyspnea, postural orthostatic tachycardia syndrome (POTS), sleep disturbances, joint pain, chest tightness.",
        "causes": "Complex etiology under active investigation: viral persistence in tissue reservoirs, chronic immune dysregulation, autoantibody production, microvascular endothelial injury, and latent viral reactivation (e.g., EBV).",
        "treatment": "Multidisciplinary individualized symptom-targeted management: activity pacing to prevent post-exertional crashes, autonomic conditioning for POTS (hydration, compression garments), pulmonary rehab, and cognitive rehabilitation.",
        "prevention": "Preventing acute SARS-CoV-2 infection through vaccination, wearing respirator masks during surges, and early antiviral treatment during acute infection which reduces Long COVID risk.",
        "content": "Post-Acute Sequelae of SARS-CoV-2 infection (PASC), commonly termed Long COVID, is diagnosed when signs and symptoms persist or emerge 4 weeks or more following initial infection. It affects individuals across all age brackets, including those with initially mild acute presentations. The condition can produce marked functional disability affecting neurological, cardiovascular, and respiratory systems. Graded exercise is frequently poorly tolerated in patients exhibiting post-exertional malaise, highlighting the necessity of structured energy-conservation pacing protocols.",
        "source": "NIH RECOVER Initiative & WHO Guidelines"
    },

    # 5. NEUROLOGICAL DISORDERS
    {
        "document_id": "DOC_026",
        "title": "Migraine Headache: Neurovascular Mechanisms and Calcitonin Gene-Related Peptide (CGRP)",
        "category": "Neurology",
        "disease": "Migraine",
        "symptoms": "Unilateral pulsating or throbbing moderate-to-severe headache, photophobia (sensitivity to light), phonophobia (sensitivity to sound), nausea, vomiting, aggravated by physical activity.",
        "causes": "Trigeminovascular system activation, release of vasodilating neuropeptides (CGRP, substance P), and cortical spreading depression. Triggers include emotional stress, sleep deprivation, hormonal fluctuations, skipped meals, and specific dietary items.",
        "treatment": "Acute abortive therapy: triptans (sumatriptan, rizatriptan), CGRP antagonists (gepants), ditans, NSAIDs; preventive therapy: beta-blockers (propranolol), topiramate, amitriptyline, botulinum toxin A, or anti-CGRP monoclonal antibodies (erenumab).",
        "prevention": "Maintaining consistent sleep schedules, regular hydration and meals, stress management techniques, avoiding known dietary triggers, and prophylactic pharmacotherapy for frequent migraines.",
        "content": "Migraine is a debilitating primary neurovascular headache disorder affecting over one billion individuals worldwide. It frequently includes distinct clinical phases: prodrome (mood changes, neck stiffness), aura (transient focal neurological visual or sensory disturbances in ~25% of patients), the headache phase lasting 4 to 72 hours, and postdrome ('migraine hangover'). Migraine with aura confers a slightly increased risk of ischemic stroke, particularly in women who smoke and use combined oral contraceptives.",
        "source": "American Migraine Foundation & NIH MedlinePlus"
    },
    {
        "document_id": "DOC_027",
        "title": "Tension-Type Headache: Diagnosis, Pericranial Tenderness, and Analgesic Stewardship",
        "category": "Neurology",
        "disease": "Tension Headache",
        "symptoms": "Bilateral, non-pulsatile, dull, aching band-like pressure around the forehead or occiput, mild-to-moderate intensity, tenderness of pericranial and trapezius musculature, lack of nausea.",
        "causes": "Heightened pericranial myofascial pain sensitivity and altered central pain processing; exacerbated by emotional stress, mental strain, poor posture, fatigue, and eye strain.",
        "treatment": "Simple analgesics such as acetaminophen, aspirin, or NSAIDs (ibuprofen, naproxen); combination analgesics with caffeine. Amitriptyline or mirtazapine for chronic prophylactic management.",
        "prevention": "Ergonomic workplace adjustments, physical therapy, stress reduction techniques, biofeedback, adequate sleep hygiene, and avoiding frequent overuse of acute analgesics.",
        "content": "Tension-type headache (TTH) is the most prevalent headache disorder globally. Unlike migraine, it is typically bilateral, non-throbbing, does not worsen with routine physical activity, and is not accompanied by nausea or vomiting. Chronic tension-type headache occurs >=15 days per month for >3 months and significantly impairs daily function. Overusing simple analgesics (>15 days/month) or combination analgesics (>10 days/month) risks inducing medication-overuse headache (rebound headache), which requires medication weaning and bridge therapy.",
        "source": "International Headache Society & Mayo Clinic"
    },
    {
        "document_id": "DOC_028",
        "title": "Parkinson's Disease: Striatal Dopamine Depletion and Movement Manifestations",
        "category": "Neurology",
        "disease": "Parkinson's Disease",
        "symptoms": "Resting tremor ('pill-rolling'), cogwheel muscle rigidity, bradykinesia (slowness of movement), postural instability, festinating gait, hypomimia (masked facies), micrographia, anosmia, constipation.",
        "causes": "Progressive degeneration of dopaminergic neurons in the substantia nigra pars compacta, associated with intracellular accumulation of misfolded alpha-synuclein aggregates (Lewy bodies).",
        "treatment": "Dopaminergic replacement therapy with levodopa/carbidopa, dopamine agonists (pramipexole, ropinirole), MAO-B inhibitors (rasagiline), COMT inhibitors; deep brain stimulation (DBS) of subthalamic nucleus in advanced stages.",
        "prevention": "No proven primary preventive measures; epidemiological associations show regular aerobic exercise and higher dietary antioxidant consumption correlate with lower prospective risk.",
        "content": "Parkinson's disease is the second most common progressive neurodegenerative disorder. Non-motor symptoms such as REM sleep behavior disorder, hyposmia, and chronic constipation often precede motor symptoms by a decade or more. As the disease advances, patients may develop motor fluctuations (wearing-off phenomena and peak-dose dyskinesias) alongside cognitive decline and autonomic dysfunction. Physical therapy, occupational therapy, and speech therapy are indispensable components of multidisciplinary care.",
        "source": "NIH National Institute of Neurological Disorders and Stroke & Mayo Clinic"
    },
    {
        "document_id": "DOC_029",
        "title": "Ischemic Stroke: Cerebrovascular Occlusion, Thrombolytic Window, and Endovascular Thrombectomy",
        "category": "Neurology",
        "disease": "Stroke",
        "symptoms": "Sudden onset of facial droop, unilateral arm or leg weakness, speech impairment (dysarthria, expressive or receptive aphasia), loss of balance, visual field loss (FAST criteria).",
        "causes": "Acute thromboembolic or atherothrombotic occlusion of an intracranial cerebral artery, interrupting cerebral blood flow and causing focal ischemic infarction.",
        "treatment": "Intravenous thrombolysis with recombinant tissue plasminogen activator (alteplase/tenecteplase) within 4.5 hours of symptom onset; mechanical endovascular thrombectomy within up to 24 hours for large vessel occlusions.",
        "prevention": "Control of hypertension, anticoagulation for atrial fibrillation, antiplatelet therapy for atherosclerotic disease, statins for hyperlipidemia, carotid endarterectomy for severe carotid stenosis, and smoking cessation.",
        "content": "Ischemic stroke accounts for approximately 85% of all acute cerebrovascular events, with the remainder caused by intracerebral or subarachnoid hemorrhage. 'Time is brain'—rapid neuroimaging with non-contrast brain CT or diffusion-weighted MRI differentiates ischemia from hemorrhage and identifies salvageable ischemic penumbra tissue. Secondary prevention protocols depend upon stroke etiology (TOAST classification: large artery atherosclerosis, cardioembolism, small vessel occlusion/lacunar, or cryptogenic).",
        "source": "American Stroke Association & WHO Guidelines"
    },
    {
        "document_id": "DOC_030",
        "title": "Epilepsy and Seizure Disorders: Epileptogenesis, Classification, and Antiseizure Medications",
        "category": "Neurology",
        "disease": "Epilepsy",
        "symptoms": "Focal motor twitches, generalized tonic-clonic convulsions (stiffening followed by rhythmic jerking), transient staring spells (absence seizures), sensory aura, postictal confusion and somnolence.",
        "causes": "Paroxysmal excessive synchronous electrical cortical neuronal discharge. Etiologies include structural lesions (stroke, traumatic brain injury, tumors), genetic channelopathies, CNS infections, or metabolic derangements.",
        "treatment": "Antiseizure medications (ASMs: levetiracetam, lamotrigine, carbamazepine, valproate); surgical resection of epileptogenic focus, vagus nerve stimulation (VNS), or ketogenic diet in refractory pediatric cases.",
        "prevention": "Preventing traumatic head injuries with helmets and seatbelts, managing infectious encephalitis promptly, avoiding seizure triggers (sleep deprivation, alcohol withdrawal, strobe lights in photosensitive epilepsy).",
        "content": "Epilepsy is defined clinically by two or more unprovoked seizures occurring more than 24 hours apart, or one unprovoked seizure with high recurrence probability. Electroencephalography (EEG) and high-resolution brain MRI are essential diagnostic investigations to classify seizures into focal or generalized onset and identify potential structural epileptogenic foci. Status epilepticus (continuous seizure activity >5 minutes) represents a critical medical emergency requiring immediate intravenous benzodiazepines followed by second-line antiepileptic infusions.",
        "source": "NIH MedlinePlus & International League Against Epilepsy"
    },

    # 6. HEMATOLOGY & NUTRITION
    {
        "document_id": "DOC_031",
        "title": "Iron Deficiency Anemia: Microcytic Hypochromic Erythropoiesis and Oral Iron Therapy",
        "category": "Hematology",
        "disease": "Iron Deficiency Anemia",
        "symptoms": "Pallor of skin and conjunctivae, chronic fatigue, dyspnea on exertion, lightheadedness, cold intolerance, brittle spoon-shaped nails (koilonychia), craving for non-food items like ice or dirt (pica), atrophic glossitis.",
        "causes": "Negative iron balance due to chronic blood loss (menorrhagia, occult gastrointestinal bleeding from ulcers or malignancy), increased physiological requirements (pregnancy, lactation), or malabsorption (celiac disease, post-gastrectomy).",
        "treatment": "Oral ferrous iron supplementation (ferrous sulfate/fumarate/gluconate) taken with vitamin C to enhance absorption; intravenous iron formulations (iron sucrose, ferric carboxymaltose) for severe intolerance or malabsorption.",
        "prevention": "Dietary consumption of iron-rich foods (lean red meats, lentils, beans, fortified cereals, dark green leafy vegetables), pairing non-heme plant iron with ascorbic acid, and screening at-risk populations.",
        "content": "Iron deficiency anemia is the single most common nutritional disorder worldwide. Lack of elemental iron impairs heme synthesis, resulting in microcytic (low MCV <80 fL), hypochromic (low MCH) erythrocytes on peripheral blood smear. Diagnostic laboratory findings include low serum ferritin (<30 ng/mL, the most sensitive indicator of depleted stores), low serum iron, elevated total iron-binding capacity (TIBC), and decreased transferrin saturation. In adult men and postmenopausal women, gastrointestinal endoscopic evaluation (colonoscopy and endoscopy) is mandatory to rule out occult neoplastic lesions.",
        "source": "WHO Guidelines & NIH MedlinePlus"
    },
    {
        "document_id": "DOC_032",
        "title": "Vitamin B12 Deficiency and Pernicious Anemia: Macrocytic Megaloblastic Hematopoiesis and Neuropathy",
        "category": "Hematology",
        "disease": "Vitamin B12 Deficiency Anemia",
        "symptoms": "Fatigue, lemon-yellow skin tint, smooth beefy red tongue (Hunter glossitis), symmetric distal paresthesias ('pins and needles'), sensory ataxia, loss of vibratory and position sense, memory loss, depression.",
        "causes": "Pernicious anemia (autoimmune destruction of gastric parietal cells causing intrinsic factor deficiency), strict unsupplemented vegan diets, terminal ileal resection, Crohn's disease, or prolonged metformin/PPI use.",
        "treatment": "Intramuscular cyanocobalamin or hydroxocobalamin injections (typically 1000 mcg daily for 1-2 weeks, followed by monthly maintenance); high-dose oral vitamin B12 (1000-2000 mcg daily) utilizing passive mucosal diffusion.",
        "prevention": "Adequate dietary intake of animal products (eggs, dairy, meat, fish), fortified nutritional yeast, and mandatory oral supplementation for strict vegan and post-bariatric surgery individuals.",
        "content": "Vitamin B12 (cobalamin) is a vital cofactor required for DNA synthesis and myelin sheath integrity. Cobalamin deficiency causes megaloblastic hematopoiesis characterized by macrocytic erythrocytes (MCV >100 fL) with hypersegmented neutrophils, alongside elevated homocysteine and methylmalonic acid (MMA) levels. Neurological sequelae, known as subacute combined degeneration of the spinal cord (affecting dorsal and lateral columns), may become irreversible if treatment is delayed. Administering folic acid alone corrects the hematological indices while allowing devastating neurological damage to silently progress.",
        "source": "NIH Office of Dietary Supplements & Mayo Clinic"
    },
    {
        "document_id": "DOC_033",
        "title": "Sickle Cell Disease: Hemoglobin S Polymerization, Vaso-Occlusive Crises, and Hydroxyurea",
        "category": "Hematology",
        "disease": "Sickle Cell Anemia",
        "symptoms": "Severe acute bone and joint pain (vaso-occlusive crises), chronic hemolytic anemia, jaundice, dactylitis in infants, splenic sequestration, pulmonary acute chest syndrome, delayed growth.",
        "causes": "Autosomal recessive point mutation in the beta-globin gene (HBB) substituting valine for glutamic acid at codon 6 (HbS), which polymerizes under hypoxic conditions.",
        "treatment": "Disease-modifying therapy with hydroxyurea (induces fetal hemoglobin HbF synthesis), L-glutamine, crizanlizumab, voxelotor; aggressive hydration and opioid analgesia for acute pain crises; blood transfusions.",
        "prevention": "Carrier screening and genetic counseling, prophylactic penicillin in early childhood to prevent pneumococcal sepsis, scheduled childhood immunizations, and avoiding severe hypoxia, dehydration, and cold exposure.",
        "content": "Sickle cell anemia is a hereditary hemoglobinopathy marked by rigid, crescent-shaped erythrocytes that obstruct microvascular capillary beds. The resultant ischemia causes excruciating vaso-occlusive pain episodes and cumulative chronic organ damage (functional asplenia, avascular bone necrosis, chronic kidney disease). Acute chest syndrome—presenting with fever, chest pain, and new pulmonary infiltrates—is a leading cause of mortality. Allogeneic hematopoietic stem cell transplantation and recent CRISPR-based gene therapies represent curative treatment options.",
        "source": "CDC & NIH National Heart, Lung, and Blood Institute"
    },
    {
        "document_id": "DOC_034",
        "title": "Vitamin D Deficiency: Calcium Homeostasis, Rickets, and Osteomalacia",
        "category": "Nutritional",
        "disease": "Vitamin D Deficiency",
        "symptoms": "Diffuse bone pain, proximal muscle weakness, generalized fatigue, frequent bone fractures; in children, skeletal deformities such as bowed legs (genu varum), knock knees (genu valgum), and rachitic rosary.",
        "causes": "Inadequate solar ultraviolet B exposure, low dietary intake of vitamin D, malabsorption syndromes (celiac, cystic fibrosis), chronic kidney disease, severe hepatic dysfunction, and dark skin pigmentation.",
        "treatment": "High-dose oral cholecalciferol (vitamin D3: 50,000 IU weekly for 8 weeks, followed by maintenance 1000-2000 IU daily), combined with adequate elemental calcium intake (1000-1200 mg daily).",
        "prevention": "Sensible sun exposure, consumption of fatty fish (salmon, mackerel), egg yolks, vitamin D-fortified dairy and plant-based milks, and routine oral supplementation for high-risk elderly or institutionalized populations.",
        "content": "Vitamin D plays an indispensable endocrine role in regulating serum calcium and phosphorus absorption across the intestinal mucosa. Deficiency (serum 25-hydroxyvitamin D <20 ng/mL or 50 nmol/L) precipitates secondary hyperparathyroidism, mobilizing calcium from bone stores. In developing pediatric skeletons, impaired growth plate mineralization produces rickets, while in adults it causes defective bone matrix mineralization termed osteomalacia, accompanied by elevated bone-specific alkaline phosphatase and increased fracture susceptibility.",
        "source": "NIH Office of Dietary Supplements & Endocrine Society"
    },
    {
        "document_id": "DOC_035",
        "title": "Scurvy: Ascorbic Acid (Vitamin C) Deficiency and Defective Collagen Synthesis",
        "category": "Nutritional",
        "disease": "Scurvy",
        "symptoms": "Perifollicular hyperkeratotic papules, corkscrew hairs, petechiae, purpura, swollen spongy bleeding gums with tooth loosening, subperiosteal hematomas, impaired wound healing, fatigue, joint effusions.",
        "causes": "Severe dietary lack of ascorbic acid (vitamin C) sustained over 1 to 3 months, seen in isolated elderly individuals, chronic alcoholics, severe psychiatric dietary restrictions, or food insecurity.",
        "treatment": "Oral ascorbic acid replenishment: 100 to 500 mg daily for children and 500 to 1000 mg daily for adults until clinical resolution; spontaneous improvement of constitutional symptoms typically occurs within 48 to 72 hours.",
        "prevention": "Regular daily dietary consumption of vitamin C-rich foods: citrus fruits (oranges, lemons, grapefruits), strawberries, kiwifruit, bell peppers, tomatoes, broccoli, and Brussels sprouts.",
        "content": "Scurvy results from severe prolonged ascorbic acid deficiency. Vitamin C acts as an essential electron donor for prolyl and lysyl hydroxylase enzymes, which are required for cross-linking and triple-helix stabilization of collagen fibrils. Defective collagen compromises blood vessel walls, skin, dentition, and osteoid tissue, producing widespread capillary fragility and hemorrhagic manifestations. Although uncommon in modern settings, scurvy continues to be diagnosed in malnourished populations and is rapidly curative upon vitamin C administration.",
        "source": "NIH MedlinePlus & British Medical Journal"
    },

    # 7. MUSCULOSKELETAL & ARTHRITIS
    {
        "document_id": "DOC_036",
        "title": "Osteoarthritis: Articular Cartilage Degradation, Joint Space Narrowing, and Physical Therapy",
        "category": "Musculoskeletal",
        "disease": "Osteoarthritis",
        "symptoms": "Deep aching joint pain exacerbated by weight-bearing and relieved by rest, joint stiffness lasting <30 minutes upon waking, crepitus, bony enlargement (Heberden and Bouchard nodes in hands), reduced range of motion.",
        "causes": "Biomechanical joint wear, aging, repetitive stress, obesity (increased mechanical load and adipokine-mediated inflammation), previous joint trauma, and female sex.",
        "treatment": "Low-impact physical therapy, weight loss, topical NSAIDs (diclofenac gel), oral NSAIDs with gastric protection, intra-articular corticosteroid injections, and total joint replacement arthroplasty for end-stage joint disease.",
        "prevention": "Maintaining a healthy body weight, avoiding repetitive occupational joint injury, strengthening quadriceps and core periarticular muscles, and engaging in low-impact aerobic activities like swimming or cycling.",
        "content": "Osteoarthritis (OA) is the most widespread degenerative joint pathology, predominantly affecting load-bearing joints (knees, hips) and hands. Progressive loss of hyaline articular cartilage is accompanied by subchondral bone sclerosis, marginal osteophyte formation, and mild synovial inflammation. Radiographic hallmarks include asymmetric joint space narrowing, subchondral sclerosis, osteophytes, and subchondral cysts. Lifestyle modification with structured exercise programs represents first-line therapy before considering surgical joint replacement.",
        "source": "American College of Rheumatology & NIH MedlinePlus"
    },
    {
        "document_id": "DOC_037",
        "title": "Rheumatoid Arthritis: Autoimmune Synovitis and Disease-Modifying Antirheumatic Drugs (DMARDs)",
        "category": "Musculoskeletal",
        "disease": "Rheumatoid Arthritis",
        "symptoms": "Symmetric polyarthritis primarily involving small joints of the hands (MCP, PIP) and wrists, prolonged morning joint stiffness (>1 hour), joint swelling and warmth, swan-neck and boutonniere deformities, rheumatoid nodules.",
        "causes": "Systemic autoimmune disorder with genetic predisposition (HLA-DRB1 shared epitope) and environmental triggers (smoking), involving autoantibodies against rheumatoid factor (RF) and citrullinated peptides (anti-CCP).",
        "treatment": "Early aggressive treatment with conventional synthetic DMARDs (methotrexate as anchor drug, leflunomide, sulfasalazine); biologic DMARDs (anti-TNF agents, rituximab, abatacept); targeted synthetic JAK inhibitors (tofacitinib).",
        "prevention": "Smoking cessation reduces risk in genetically susceptible individuals; early identification and intervention during the 'window of opportunity' prevents irreversible joint erosion and deformity.",
        "content": "Rheumatoid arthritis (RA) is a chronic systemic autoimmune inflammatory disease characterized by persistent proliferative synovitis (pannus formation) that invades and destroys underlying cartilage and bone. Extra-articular manifestations include rheumatoid lung nodules, interstitial lung disease, pericarditis, scleritis, and accelerated cardiovascular disease. Serum anti-CCP antibodies provide high diagnostic specificity (~95%). Initiating DMARD therapy within 3 months of symptom onset is vital to achieve clinical remission and preserve functional capacity.",
        "source": "American College of Rheumatology & Mayo Clinic"
    },
    {
        "document_id": "DOC_038",
        "title": "Gouty Arthritis: Hyperuricemia, Monosodium Urate Crystal Deposition, and Colchicine",
        "category": "Musculoskeletal",
        "disease": "Gout",
        "symptoms": "Excruciating acute inflammatory monarthritis, classical severe pain, redness, swelling, and extreme warmth over the first metatarsophalangeal joint (podagra), fever, formation of chalky tophi in chronic stages.",
        "causes": "Deposition of needle-shaped monosodium urate crystals in synovial fluid secondary to chronic hyperuricemia (serum urate >6.8 mg/dL). Triggers include high purine diet (organ meats, seafood), alcohol (beer), fructose, diuretics, and renal insufficiency.",
        "treatment": "Acute flare management: oral colchicine, NSAIDs (indomethacin, naproxen), or systemic/intra-articular corticosteroids; long-term urate-lowering therapy (ULT): xanthine oxidase inhibitors (allopurinol, febuxostat) targeting serum urate <6.0 mg/dL.",
        "prevention": "Limiting intake of purine-rich meats, reducing alcohol and high-fructose corn syrup consumption, maintaining adequate hydration, weight management, and avoiding abrupt changes in uric acid levels without anti-inflammatory flare prophylaxis.",
        "content": "Gout is a painful crystal-induced arthropathy. Polarized light microscopy of synovial fluid aspirate provides definitive confirmation by demonstrating negatively birefringent needle-shaped intracellular monosodium urate crystals. In chronic uncontrolled gout, aggregated urate deposits form painless or destructive tophi around joints, the ear helix, and olecranon bursae. Initiating urate-lowering therapy requires concomitant anti-inflammatory prophylaxis (low-dose colchicine or NSAIDs) for 3-6 months to prevent mobilization flares.",
        "source": "NIH MedlinePlus & American College of Rheumatology"
    },
    {
        "document_id": "DOC_039",
        "title": "Ankylosing Spondylitis: Axial Spondyloarthritis, HLA-B27, and Sacroiliitis",
        "category": "Musculoskeletal",
        "disease": "Ankylosing Spondylitis",
        "symptoms": "Chronic inflammatory back pain starting before age 45, morning stiffness >45 minutes improved by physical exercise and not relieved by rest, night awakenings, alternating buttock pain, reduced lumbar spinal flexion, enthesitis.",
        "causes": "Strong genetic predisposition strongly linked with human leukocyte antigen HLA-B27, leading to immune-mediated entheseal inflammation and new bone formation (syndesmophytes).",
        "treatment": "First-line therapy: regular daily exercise and high-dose NSAIDs; for refractory axial disease: biologic TNF inhibitors (infliximab, adalimumab) or IL-17 inhibitors (secukinumab).",
        "prevention": "No established primary prevention; lifelong physical therapy and posture training are essential to maintain spinal mobility and prevent severe thoracic kyphotic curvature and spinal fusion.",
        "content": "Ankylosing spondylitis (AS) is a chronic inflammatory seronegative spondyloarthropathy primarily affecting the sacroiliac joints and axial skeleton. Over decades, persistent inflammation leads to ossification of spinal ligaments and intervertebral joints, culminating in rigid spinal fusion ('bamboo spine' appearance on radiography). Extra-skeletal features include acute anterior uveitis (eye redness and pain), apical pulmonary fibrosis, aortic insufficiency, and secondary osteoporosis.",
        "source": "Spondylitis Association of America & NHS"
    },
    {
        "document_id": "DOC_040",
        "title": "Osteoporosis: Bone Mineral Density Depletion, T-scores, and Bisphosphonate Therapy",
        "category": "Musculoskeletal",
        "disease": "Osteoporosis",
        "symptoms": "Asymptomatic until fracture occurs ('silent thief of bone'); manifestations of vertebral compression fractures include sudden back pain, loss of height, and progressive dorsal kyphosis ('dowager's hump').",
        "causes": "Imbalance between osteoclast-mediated bone resorption and osteoblast-mediated bone formation, exacerbated by postmenopausal estrogen decline, aging, chronic glucocorticoid therapy, smoking, and low dietary calcium/vitamin D.",
        "treatment": "Antiresorptive agents: bisphosphonates (alendronate, zoledronic acid), denosumab (RANKL inhibitor); anabolic bone-forming agents: teriparatide, abaloparatide, romosozumab; daily calcium and vitamin D supplementation.",
        "prevention": "Regular weight-bearing and resistance exercises, adequate lifetime dietary calcium (1200 mg/day) and vitamin D (800-1000 IU/day), smoking cessation, limiting alcohol intake, and fall prevention strategies in the home.",
        "content": "Osteoporosis is a systemic skeletal disease characterized by low bone mass and microarchitectural deterioration of bone tissue, causing heightened bone fragility and susceptibility to low-trauma fragility fractures (most commonly hip, spine, and wrist). Diagnosis is established via Dual-energy X-ray Absorptiometry (DEXA) scanning: a bone mineral density T-score <= -2.5 defines osteoporosis. The FRAX tool evaluates 10-year fracture probabilities to guide pharmacotherapeutic thresholds.",
        "source": "National Osteoporosis Foundation & NIH MedlinePlus"
    },

    # 8. GASTROENTEROLOGY
    {
        "document_id": "DOC_041",
        "title": "Acute and Chronic Gastritis: Mucosal Inflammation and Helicobacter pylori Infection",
        "category": "Gastroenterology",
        "disease": "Gastritis",
        "symptoms": "Epigastric burning or gnawing abdominal pain, postprandial fullness, early satiety, nausea, vomiting, belching, bloating, anorexia; gastrointestinal bleeding may cause melena.",
        "causes": "Infection with Helicobacter pylori bacteria, frequent use of nonsteroidal anti-inflammatory drugs (NSAIDs like ibuprofen, naproxen), excessive alcohol ingestion, severe physiologic stress, and autoimmune gastritis.",
        "treatment": "Eradication therapy for H. pylori using 14-day quadruple therapy (PPI, bismuth subcitrate, metronidazole, tetracycline); proton pump inhibitors (omeprazole, pantoprazole), H2-blockers, and discontinuing offending NSAIDs.",
        "prevention": "Practicing good hand hygiene and sanitation to prevent H. pylori transmission, minimizing chronic NSAID use or co-prescribing gastroprotective agents, avoiding excessive alcohol, and smoking cessation.",
        "content": "Gastritis refers to histologically confirmed inflammation of the gastric mucosa. While acute gastritis often results from chemical insults (NSAIDs, alcohol) leading to mucosal erosion, chronic gastritis is predominantly driven by chronic Helicobacter pylori colonization of the gastric antrum and body. H. pylori utilizes urease to neutralize stomach acid and establish persistent colonization. Untreated chronic H. pylori gastritis induces mucosal atrophy and intestinal metaplasia, serving as a well-documented precursor to gastric adenocarcinoma and MALT lymphoma.",
        "source": "NIH MedlinePlus & American Gastroenterological Association"
    },
    {
        "document_id": "DOC_042",
        "title": "Peptic Ulcer Disease: Gastric versus Duodenal Ulcers, Endoscopy, and Complications",
        "category": "Gastroenterology",
        "disease": "Peptic Ulcer Disease",
        "symptoms": "Epigastric pain; duodenal ulcers characteristically produce burning hunger pain 2-3 hours postprandially relieved by food or antacids, while gastric ulcer pain is often provoked by eating. Complications present with hematemesis or coffee-ground emesis.",
        "causes": "Helicobacter pylori infection and NSAID use disrupt mucosal defense mechanisms; uncommon causes include gastrinoma (Zollinger-Ellison syndrome), smoking, and severe physiologic stress.",
        "treatment": "High-dose proton pump inhibitors (PPIs) for 4 to 8 weeks, confirmed H. pylori eradication therapy, endoscopic hemostatic clipping or thermocoagulation for bleeding ulcers, and avoidance of ulcerogenic medications.",
        "prevention": "Testing for and eradicating H. pylori in patients requiring long-term NSAID or antiplatelet therapy, utilizing selective COX-2 inhibitors with PPIs when NSAIDs are unavoidable, and smoking cessation.",
        "content": "Peptic ulcer disease (PUD) involves mucosal ulcerations extending through the muscularis mucosae into deeper layers of the stomach or proximal duodenum. Upper gastrointestinal endoscopy (esophagogastroduodenoscopy, EGD) is the diagnostic procedure of choice, enabling direct visualization, mucosal biopsy for rapid urease testing, and immediate therapeutic hemostasis. Major life-threatening complications include acute upper gastrointestinal hemorrhage, visceral perforation presenting with acute peritonitis and free air under the diaphragm, and gastric outlet obstruction.",
        "source": "American College of Gastroenterology & Mayo Clinic"
    },
    {
        "document_id": "DOC_043",
        "title": "Gastroesophageal Reflux Disease (GERD): Acid Reflux, Barrett's Esophagus, and PPI Therapy",
        "category": "Gastroenterology",
        "disease": "GERD",
        "symptoms": "Heartburn (pyrosis: retrosternal burning pain after meals), acid regurgitation, dysphagia, globus sensation, chronic dry cough, hoarseness, water brash, asthma exacerbations.",
        "causes": "Transient lower esophageal sphincter (LES) relaxations, low basal LES resting tone, hiatal hernia, delayed gastric emptying, increased intra-abdominal pressure due to obesity or pregnancy.",
        "treatment": "Proton pump inhibitors (omeprazole, esomeprazole), H2-receptor antagonists (famotidine), antacids; anti-reflux surgery (laparoscopic Nissen fundoplication or magnetic sphincter augmentation) for refractory cases.",
        "prevention": "Weight reduction in overweight individuals, elevating the head of the bed by 6 inches, avoiding lying down within 3 hours of meals, and eliminating dietary triggers (chocolate, caffeine, fatty foods, peppermint, alcohol).",
        "content": "Gastroesophageal reflux disease (GERD) is a chronic disorder in which the retrograde flow of acidic gastric contents into the esophagus causes troublesome symptoms or mucosal damage. Long-standing chronic acid exposure can produce erosive esophagitis, peptic strictures, and specialized intestinal metaplasia known as Barrett's esophagus. Patients with Barrett's esophagus require regular endoscopic surveillance with biopsies due to an increased risk of progression to esophageal adenocarcinoma.",
        "source": "NIH MedlinePlus & American College of Gastroenterology"
    },
    {
        "document_id": "DOC_044",
        "title": "Food Poisoning: Bacterial Enterotoxins and Acute Gastroenteritis",
        "category": "Gastroenterology",
        "disease": "Food Poisoning",
        "symptoms": "Acute onset of nausea, violent vomiting, crampy abdominal pain, watery or bloody diarrhea, low-grade fever, headache, weakness, signs of dehydration (dry mucous membranes, tachycardia).",
        "causes": "Ingestion of food contaminated by preformed toxins (Staphylococcus aureus, Bacillus cereus) producing rapid onset within 1-6 hours, or foodborne pathogens (Salmonella, Campylobacter, E. coli, Norovirus, Listeria).",
        "treatment": "Oral rehydration solution (ORS) with balanced electrolytes and glucose; intravenous isotonic fluids for severe dehydration; empiric antibiotics (azithromycin or fluoroquinolones) reserved for severe invasive bacterial diarrhea.",
        "prevention": "Adhering to food safety: cooking poultry and meats to safe internal temperatures, separating raw meats from produce, prompt refrigeration of leftovers (<4°C/40°F), washing hands and surfaces thoroughly.",
        "content": "Food poisoning is an acute gastrointestinal illness resulting from the consumption of foods contaminated with microbes or their toxins. Distinguishing toxin-mediated syndromes (short incubation <6 hours, prominent vomiting) from invasive or non-invasive infections (longer incubation >16 hours, diarrhea, fever) aids clinical triage. Most episodes are self-limiting and resolve within 24 to 72 hours with supportive hydration. Antidiarrheal agents (loperamide) must be avoided in patients with high fever or bloody diarrhea (dysentery) to prevent toxin retention.",
        "source": "CDC & WHO Food Safety Guidelines"
    },
    {
        "document_id": "DOC_045",
        "title": "Botulism: Clostridium botulinum Neurotoxin and Descending Flaccid Paralysis",
        "category": "Gastroenterology",
        "disease": "Botulism",
        "symptoms": "Symmetrical descending flaccid paralysis: early cranial nerve palsies with blurred vision, diplopia, ptosis, dysarthria, dysphagia, followed by bilateral symmetrical weakness, respiratory depression.",
        "causes": "Absorption of potent botulinum neurotoxin produced by the anaerobic spore-forming bacterium Clostridium botulinum; types include foodborne (home-canned foods), infant botulism (ingesting honey spores), and wound botulism.",
        "treatment": "Immediate emergency administration of equine heptavalent botulinum antitoxin or human botulism immune globulin (BabyBIG for infants); supportive mechanical ventilation and intensive hemodynamic monitoring.",
        "prevention": "Following strict pressure-cooking protocols for home-canned low-acid foods, boiling home-canned foods for 10 minutes before consumption to denature heat-labile toxin, never feeding honey to infants under 1 year of age.",
        "content": "Botulism is a rare but life-threatening neuroparalytic syndrome caused by botulinum neurotoxins—the most potent biological toxins known. The toxin irreversibly cleaves SNARE proteins at presynaptic cholinergic neuromuscular junctions, blocking acetylcholine release. Clinical presentation features symmetric, descending motor weakness with intact sensory perception and alert mental status. Prompt clinical diagnosis without waiting for laboratory bioassay results is imperative because antitoxin only halts progression by neutralizing circulating, unbound neurotoxin.",
        "source": "CDC & World Health Organization"
    },

    # 9. NEPHROLOGY & KIDNEY DISEASE
    {
        "document_id": "DOC_046",
        "title": "Chronic Kidney Disease: Staging, Glomerular Filtration Rate, and Renoprotection",
        "category": "Nephrology",
        "disease": "Chronic Kidney Disease",
        "symptoms": "Often asymptomatic in early stages (stages 1-3); advanced stages manifest with fatigue, anorexia, nausea, pruritus, metallic taste, peripheral and periorbital edema, nocturia, hypertension, uremic frost.",
        "causes": "Leading causes are diabetic nephropathy and hypertensive nephrosclerosis; other causes include chronic glomerulonephritis, polycystic kidney disease, chronic interstitial nephritis, and recurrent pyelonephritis.",
        "treatment": "Blood pressure control (<130/80 mmHg) using ACE inhibitors or ARBs, SGLT2 inhibitors (dapagliflozin/empagliflozin) for renoprotection, nonsteroidal mineralocorticoid antagonists (finerenone), dietary protein and sodium restriction, renal replacement therapy (dialysis or kidney transplant) for end-stage kidney disease (ESKD).",
        "prevention": "Strict glycemic control in diabetes (HbA1c <7%), optimal blood pressure control, avoidance of nephrotoxic medications (frequent NSAIDs, IV iodinated contrast without hydration), and annual screening with urine albumin-to-creatinine ratio (uACR).",
        "content": "Chronic kidney disease (CKD) is defined as abnormalities of kidney structure or function persisting for >3 months, staged primarily by estimated glomerular filtration rate (eGFR) and albuminuria levels. Progressive decline in nephron mass leads to systemic retention of uremic toxins, anemia secondary to deficient erythropoietin production, and mineral and bone disorder (CKD-MBD) caused by hyperphosphatemia and hypocalcemia. Interventions targeting hemodynamic intraglomerular pressure reduction delay progression to end-stage renal failure.",
        "source": "KDIGO Guidelines & National Kidney Foundation"
    },
    {
        "document_id": "DOC_047",
        "title": "Acute Kidney Injury: Prerenal, Intrinsic, and Postrenal Pathophysiology",
        "category": "Nephrology",
        "disease": "Acute Kidney Injury",
        "symptoms": "Abrupt decrease in urine output (oliguria <400 mL/day or anuria), fluid retention causing peripheral edema and dyspnea, nausea, fatigue, confusion, asterixis, metabolic acidosis, hyperkalemia.",
        "causes": "Prerenal azotemia (hypovolemia, sepsis, heart failure, renal artery stenosis); intrinsic renal injury (acute tubular necrosis [ATN] from ischemia or nephrotoxins, acute interstitial nephritis, glomerulonephritis); postrenal obstruction (BPH, bilateral ureteral stones).",
        "treatment": "Treating underlying cause: intravenous crystalloid volume expansion in prerenal azotemia; discontinuing nephrotoxic drugs; relieving urinary tract obstruction via catheterization or nephrostomy; urgent hemodialysis for refractory hyperkalemia, severe metabolic acidosis, or fluid overload.",
        "prevention": "Adequate hydration before surgical procedures and radiographic contrast administration, therapeutic drug monitoring of nephrotoxic antibiotics (vancomycin, aminoglycosides), and monitoring renal function in critically ill patients.",
        "content": "Acute kidney injury (AKI) is an abrupt decline in renal filtration function occurring over hours to days, diagnosed by an acute rise in serum creatinine (>=0.3 mg/dL within 48 hours) or reduction in urine output. Prerenal causes show high urine osmolality and fractional excretion of sodium (FeNa) <1%, indicating intact tubular reabsorptive capacity, whereas intrinsic ATN demonstrates muddy brown granular casts on urine microscopy with FeNa >2%. Prompt differentiation prevents transition from reversible prerenal hypoperfusion to ischemic ATN.",
        "source": "KDIGO Clinical Practice Guideline & NIH MedlinePlus"
    },
    {
        "document_id": "DOC_048",
        "title": "Nephrolithiasis: Renal Calculi Types, Hydronephrosis, and Extracorporeal Shock Wave Lithotripsy",
        "category": "Nephrology",
        "disease": "Kidney Stones",
        "symptoms": "Severe, sudden paroxysmal colicky flank pain radiating along the groin and labia/testicle ('renal colic'), gross or microscopic hematuria, dysuria, urinary frequency, nausea, vomiting, restlessness.",
        "causes": "Urinary supersaturation of stone-forming salts: calcium oxalate (most common, ~75%), calcium phosphate, uric acid, struvite (infection stones caused by urease-producing Proteus), or cystine; low fluid intake.",
        "treatment": "Parenteral NSAIDs (ketorolac) or opioids for acute pain control; medical expulsive therapy with alpha-blockers (tamsulosin) for small stones (<6 mm); extracorporeal shock wave lithotripsy (ESWL), ureteroscopy with laser lithotripsy, or percutaneous nephrolithotomy (PCNL) for larger obstructing stones.",
        "prevention": "High daily fluid intake (>=2.5-3 liters/day to ensure dilute urine), reducing dietary sodium and animal purines, maintaining normal dietary calcium intake, and potassium citrate supplementation for hypocitraturia or uric acid stones.",
        "content": "Nephrolithiasis is a common urological disorder involving crystal aggregations forming within the renal calyces and pelvis. When calculi dislodge into the ureter, acute obstruction produces ureteral spasm and proximal hydronephrosis responsible for severe colic pain. Non-contrast helical CT of the abdomen and pelvis is the gold standard imaging modality, identifying stone location, size, and secondary hydroureter. Obstructing stones accompanied by proximal urinary tract infection represent a surgical emergency requiring urgent decompression.",
        "source": "American Urological Association & Mayo Clinic"
    },
    {
        "document_id": "DOC_049",
        "title": "Nephrotic Syndrome: Massive Proteinuria, Hypoalbuminemia, and Hyperlipidemia",
        "category": "Nephrology",
        "disease": "Nephrotic Syndrome",
        "symptoms": "Severe generalized pitting edema (anasarca, periorbital morning puffiness, scrotal/labial swelling, ascites), foamy urine, fatigue, loss of appetite, heightened susceptibility to bacterial infections.",
        "causes": "Glomerular podocyte effacement and filtration barrier breakdown. Primary causes: Minimal Change Disease (pediatric), Focal Segmental Glomerulosclerosis (FSGS), Membranous Nephropathy; Secondary: Diabetic nephropathy, Lupus nephritis, Amyloidosis.",
        "treatment": "Corticosteroid therapy (prednisone) as first-line in minimal change disease; immunosuppressive agents (calcineurin inhibitors, cyclophosphamide, rituximab); loop diuretics for edema; ACE inhibitors/ARBs for proteinuria reduction; statins for hyperlipidemia; prophylactic anticoagulation in high-risk membranous nephropathy.",
        "prevention": "Optimizing glycemic and blood pressure control in systemic disorders, prompt evaluation of persistent facial puffiness in children, and adherence to prescribed immunosuppression regimens to prevent relapses.",
        "content": "Nephrotic syndrome is a classic clinical triad characterized by nephrotic-range proteinuria (>3.5 grams per 24 hours per 1.73 m²), hypoalbuminemia (<3.0 g/dL), and generalized edema, accompanied by hyperlipidemia and lipiduria (oval fat bodies exhibiting 'Maltese cross' appearance under polarized light). Urinary loss of antithrombin III and plasminogen leads to a hypercoagulable state with elevated risk of deep vein thrombosis and renal vein thrombosis. Renal biopsy with light, immunofluorescence, and electron microscopy is the definitive diagnostic standard in adults.",
        "source": "NIH MedlinePlus & KDIGO"
    },
    {
        "document_id": "DOC_050",
        "title": "Autosomal Dominant Polycystic Kidney Disease (ADPKD): Cystogenesis and Tolvaptan",
        "category": "Nephrology",
        "disease": "Polycystic Kidney Disease",
        "symptoms": "Bilateral flank or abdominal pain, palpable enlarged kidneys, recurrent urinary tract infections, gross hematuria from cyst rupture, early-onset hypertension, nephrolithiasis.",
        "causes": "Autosomal dominant mutations in the PKD1 (chromosome 16, ~85% of cases) or PKD2 (chromosome 4, ~15% of cases) genes, which encode polycystin-1 and polycystin-2 membrane proteins.",
        "treatment": "Blood pressure management (<110/75 mmHg in young adults) using ACE inhibitors or ARBs, high fluid intake to suppress endogenous vasopressin, tolvaptan (vasopressin V2 receptor antagonist) to slow cyst growth, pain management, and renal replacement therapy when end-stage kidney failure supervenes.",
        "prevention": "Genetic counseling for affected families, screening at-risk relatives with renal ultrasound, avoiding nephrotoxic agents, and maintaining high fluid intake to suppress vasopressin-mediated cyst fluid accumulation.",
        "content": "Autosomal Dominant Polycystic Kidney Disease (ADPKD) is the most common monogenic cause of kidney failure. Mutations lead to dysregulated tubular epithelial cell proliferation and continuous fluid secretion, generating countless expanding fluid-filled cysts that progressively destroy functioning renal parenchyma over decades. Extrarenal manifestations include hepatic cysts (polycystic liver), pancreatic cysts, mitral valve prolapse, colonic diverticula, and intracranial berry aneurysms of the circle of Willis, which carry risk of subarachnoid hemorrhage.",
        "source": "National Kidney Foundation & Mayo Clinic"
    },

    # 10. HEPATOLOGY & LIVER DISEASE
    {
        "document_id": "DOC_051",
        "title": "Metabolic Dysfunction-Associated Steatotic Liver Disease (MASLD / NAFLD): Steatohepatitis and Fibrosis",
        "category": "Hepatology",
        "disease": "Fatty Liver Disease",
        "symptoms": "Usually asymptomatic; mild dull right upper quadrant discomfort, fatigue, malaise; hepatomegaly on physical examination in early stages; spider angiomas, palmar erythema in advanced cirrhosis.",
        "causes": "Hepatic triglyceride accumulation associated with insulin resistance, obesity, type 2 diabetes mellitus, dyslipidemia, and metabolic syndrome.",
        "treatment": "Lifestyle modification with 7-10% sustained total body weight loss through hypocaloric diet and exercise; bariatric surgery in eligible candidates; resmetirom (thyroid hormone receptor-beta agonist) in non-cirrhotic NASH with moderate-to-advanced fibrosis; managing diabetes and hyperlipidemia.",
        "prevention": "Consuming a Mediterranean-style diet, avoiding sugar-sweetened beverages and high-fructose corn syrup, regular physical activity (>=150 min/week), and maintaining normal body mass index.",
        "content": "Non-Alcoholic Fatty Liver Disease (NAFLD), recently reclassified as Metabolic Dysfunction-Associated Steatotic Liver Disease (MASLD), encompasses a spectrum from simple steatosis to Metabolic Dysfunction-Associated Steatohepatitis (MASH / NASH). In MASH, fat accumulation is complicated by lobular inflammation, hepatocyte ballooning, and progressive collagen fibrosis. Non-invasive scoring tools (FIB-4 index, NAFLD fibrosis score) and vibration-controlled transient elastography (FibroScan) assess hepatic stiffness to stratify fibrosis risk without liver biopsy.",
        "source": "AASLD Guidelines & NIH MedlinePlus"
    },
    {
        "document_id": "DOC_052",
        "title": "Liver Cirrhosis: Portal Hypertension, Ascites, and Hepatic Encephalopathy",
        "category": "Hepatology",
        "disease": "Cirrhosis",
        "symptoms": "Jaundice (icterus), abdominal distension from ascites, peripheral edema, spider telangiectasias, caput medusae, palmar erythema, gynecomastia, asterixis ('flapping tremor'), easy bruising, confusion.",
        "causes": "End-stage outcome of chronic liver injury: chronic hepatitis B or C infection, chronic alcohol-associated liver disease, advanced MASLD/MASH, autoimmune hepatitis, and primary biliary cholangitis.",
        "treatment": "Managing portal hypertension: non-selective beta-blockers (propranolol, carvedilol) and endoscopic variceal band ligation; managing ascites: sodium restriction and spironolactone plus furosemide; managing encephalopathy: lactulose and rifaximin; definitive cure via orthotopic liver transplantation.",
        "prevention": "Hepatitis B vaccination, treatment of chronic hepatitis B/C with antivirals, abstaining from alcohol abuse, managing metabolic risk factors, and semiannual ultrasound screening for hepatocellular carcinoma.",
        "content": "Liver cirrhosis is characterized by diffuse architectural distortion with regenerative parenchymal nodules surrounded by dense fibrous septa. Fibrosis increases intrahepatic vascular resistance, generating portal hypertension (hepatic venous pressure gradient >=10 mmHg). Critical decompensations include bleeding gastroesophageal varices, spontaneous bacterial peritonitis (SBP), hepatorenal syndrome, and hepatic encephalopathy resulting from impaired clearance of gut-derived neurotoxins such as ammonia. The Child-Pugh and MELD-Na scores quantify liver disease severity.",
        "source": "AASLD Guidelines & Mayo Clinic"
    },
    {
        "document_id": "DOC_053",
        "title": "Viral Hepatitis B: Chronic Infection, Serological Markers, and Nucleoside Analogs",
        "category": "Hepatology",
        "disease": "Hepatitis B",
        "symptoms": "Acute infection: malaise, anorexia, nausea, dark tea-colored urine, clay-colored stools, jaundice, right upper quadrant pain. Chronic infection is often clinically silent until cirrhosis or hepatocellular carcinoma develops.",
        "causes": "Hepatitis B virus (HBV), a partially double-stranded DNA hepadnavirus transmitted via percutaneous or mucosal exposure to infective blood or body fluids (perinatal/vertical transmission, sexual contact, contaminated needles).",
        "treatment": "Oral nucleoside/nucleotide reverse transcriptase inhibitors with high barrier to resistance (entecavir, tenofovir disoproxil, tenofovir alafenamide) to suppress HBV viral replication; pegylated interferon alfa-2a.",
        "prevention": "Universal Hepatitis B vaccination (birth dose followed by 2-3 dose series), Hepatitis B immune globulin (HBIG) administered to neonates born to HBsAg-positive mothers within 12 hours of delivery, safe injection practices, and barrier contraception.",
        "content": "Hepatitis B virus infection is a major cause of chronic liver disease, cirrhosis, and primary liver cancer worldwide. Diagnosis relies on serological panels: Hepatitis B surface antigen (HBsAg) indicates active infection; anti-HBs indicates immunity; anti-HBc IgM signifies acute infection; HBeAg denotes high viral replication and infectivity. Progression to chronicity occurs in >90% of perinatally infected infants but only ~5% of immunocompetent adults. Long-term antiviral therapy suppresses serum HBV DNA and reduces cirrhosis progression.",
        "source": "WHO Guidelines & CDC"
    },
    {
        "document_id": "DOC_054",
        "title": "Viral Hepatitis C: Direct-Acting Antivirals (DAAs) and Sustained Virologic Response",
        "category": "Hepatology",
        "disease": "Hepatitis C",
        "symptoms": "Acute infection is asymptomatic in ~75-80% of individuals; chronic infection produces non-specific fatigue, arthralgias, and cognitive clouding until cirrhosis or liver failure manifests with jaundice and ascites.",
        "causes": "Hepatitis C virus (HCV), a positive-sense single-stranded RNA flavivirus transmitted predominantly through parenterally contaminated blood (injection drug use, non-sterile medical procedures, unscreened blood transfusions prior to 1992).",
        "treatment": "All-oral, pangenotypic direct-acting antiviral (DAA) combination regimens (sofosbuvir-velpatasvir, glecaprevir-pibrentasvir) administered for 8 to 12 weeks, achieving cure rates exceeding 95%.",
        "prevention": "No effective vaccine exists due to high HCV genetic hypervariability; prevention relies on harm reduction needle-exchange programs, sterile healthcare injection protocols, universal blood donor screening, and barrier precautions.",
        "content": "Hepatitis C virus causes both acute and chronic hepatitis, with chronicity developing in 70-85% of untreated individuals. Historically treated with poorly tolerated interferon-based regimens, HCV management underwent a revolution with the advent of direct-acting antivirals targeting viral NS3/4A protease, NS5A replication complex, and NS5B RNA-dependent RNA polymerase. Achieving a sustained virologic response (undetectable HCV RNA 12 weeks post-treatment, SVR12) equates to a virological cure and dramatically reduces future cirrhosis and mortality.",
        "source": "AASLD-IDSA Guidelines & WHO"
    },
    {
        "document_id": "DOC_055",
        "title": "Alcohol-Associated Liver Disease: Alcoholic Hepatitis, Steatosis, and Maddrey's Discriminant Function",
        "category": "Hepatology",
        "disease": "Alcoholic Hepatitis",
        "symptoms": "Rapid-onset jaundice, fever, anorexia, abdominal distension, tender hepatomegaly, ascites, muscle wasting, signs of portal hypertension, hepatic encephalopathy.",
        "causes": "Chronic heavy ethanol consumption (>40-80 g/day for men, >20-40 g/day for women over decades). Ethanol metabolism by alcohol dehydrogenase generates acetaldehyde, producing oxidative stress, mitochondrial injury, and steatonecrosis.",
        "treatment": "Absolute, permanent cessation of alcohol; nutritional support with enteral feeding; for severe alcoholic hepatitis (Maddrey's Discriminant Function >=32): corticosteroid therapy (prednisolone 40 mg daily for 28 days) if no active infection or gastrointestinal bleeding.",
        "prevention": "Abstinence from alcohol or adherence to low-risk drinking guidelines, screening for alcohol use disorder with AUDIT questionnaires, and psychosocial rehabilitation support groups.",
        "content": "Alcohol-associated liver disease (ALD) spans a spectrum from simple alcoholic fatty liver to acute alcoholic hepatitis and decompensated cirrhosis. Acute alcoholic hepatitis represents an acute inflammatory flare characterized by neutrophilic infiltration, hepatocyte ballooning with Mallory-Denk bodies, and pericellular 'chicken-wire' fibrosis. The Maddrey Discriminant Function (DF) and the Lille Model guide the initiation and continuation of corticosteroid therapy, identifying non-responders to prevent futile immunosuppression.",
        "source": "AASLD Guidelines & NIH National Institute on Alcohol Abuse and Alcoholism"
    },

    # 11. IMMUNOLOGY & ALLERGIC DISORDERS
    {
        "document_id": "DOC_056",
        "title": "Allergic Rhinitis: IgE-Mediated Type I Hypersensitivity and Intranasal Corticosteroids",
        "category": "Allergy & Immunology",
        "disease": "Allergic Rhinitis",
        "symptoms": "Paroxysmal sneezing, clear rhinorrhea, nasal itching, bilateral nasal congestion, itchy watery eyes (allergic conjunctivitis), dark under-eye circles ('allergic shiners'), transverse nasal crease.",
        "causes": "Type I hypersensitivity reaction mediated by allergen-specific IgE antibodies bound to high-affinity Fc receptors on mucosal mast cells. Triggers include pollens (grass, trees, weeds), house dust mites, animal dander, and fungal spores.",
        "treatment": "Intranasal corticosteroids (fluticasone, mometasone) as the most effective single pharmacotherapy; second-generation non-sedating oral antihistamines (cetirizine, fexofenadine, loratadine); intranasal antihistamines (azelastine); allergen immunotherapy (AIT: sublingual or subcutaneous).",
        "prevention": "Allergen avoidance: keeping windows closed during high pollen counts, using high-efficiency particulate air (HEPA) filters, encasing pillows and mattresses in allergen-impermeable covers, and washing bedding in hot water weekly.",
        "content": "Allergic rhinitis is an extremely common inflammatory disorder of the nasal mucosa provoked by allergen exposure. Upon contact with sensitized nasal mucosa, cross-linking of surface-bound IgE molecules triggers immediate mast cell degranulation, releasing preformed mediators including histamine, leukotrienes, and prostaglandins that cause immediate pruritus and vasodilatation. A late-phase reaction develops 4 to 8 hours later, driven by eosinophil and T-lymphocyte infiltration causing prolonged nasal blockage.",
        "source": "American Academy of Allergy, Asthma & Immunology & NIH MedlinePlus"
    },
    {
        "document_id": "DOC_057",
        "title": "Anaphylaxis: Systemic IgE-Mediated Degranulation and Intramuscular Epinephrine Protocol",
        "category": "Allergy & Immunology",
        "disease": "Anaphylaxis",
        "symptoms": "Urticaria (hives), generalized flushing, intense pruritus, angioedema (swelling of lips, tongue, uvula), laryngeal stridor, bronchospasm with wheezing, hypotension, cardiovascular syncope, crampy abdominal pain, vomiting.",
        "causes": "Systemic mast cell and basophil degranulation triggered by specific allergens: food allergens (peanuts, tree nuts, shellfish, milk, eggs), venomous insect stings (hymenoptera: bees, wasps), medications (penicillin, cephalosporins, NSAIDs), and natural rubber latex.",
        "treatment": "Immediate intramuscular epinephrine (0.3 mg for adults, 0.15 mg for children) injected into the anterolateral mid-thigh; place patient recumbent with legs elevated; high-flow oxygen; intravenous crystalloid fluids for hypotension; second-line adjuncts: H1/H2 antihistamines and corticosteroids.",
        "prevention": "Strict avoidance of known causative allergens, carrying two unexpired epinephrine auto-injectors (EpiPen, Auvi-Q) at all times, wearing medical alert identification, and venom immunotherapy (VIT) for sting allergies.",
        "content": "Anaphylaxis is an acute, severe, potentially fatal multi-system hypersensitivity reaction that can develop within seconds to minutes of allergen exposure. Epinephrine is the only definitive life-saving medication; it acts on alpha-1 receptors to reverse peripheral vasodilatation and reduce mucosal edema, beta-1 receptors to increase cardiac contractility, and beta-2 receptors to produce bronchodilation and attenuate further mediator release. Delaying epinephrine administration is the primary contributor to fatal anaphylactic outcomes.",
        "source": "World Allergy Organization & CDC"
    },
    {
        "document_id": "DOC_058",
        "title": "Atopic Dermatitis (Eczema): Epidermal Barrier Dysfunction, Filaggrin Mutations, and Topical Calcineurin Inhibitors",
        "category": "Allergy & Immunology",
        "disease": "Atopic Dermatitis",
        "symptoms": "Intense intractable pruritus ('the itch that rashes'), erythematous dry scaly papules and plaques, lichenification (skin thickening from chronic scratching), excoriations; predilection for flexural creases (antecubital and popliteal fossae) in adults and facial/extensor surfaces in infants.",
        "causes": "Impaired skin barrier function due to genetic loss-of-function mutations in the filaggrin (FLG) gene, accompanied by Th2-skewed immune dysregulation and cutaneous microbiome dysbiosis (colonization by Staphylococcus aureus).",
        "treatment": "Frequent generous application of bland emollient ointments, topical corticosteroids (triamcinolone, hydrocortisone), topical calcineurin inhibitors (tacrolimus, pimecrolimus), PDE4 inhibitors (crisaborole); biologic IL-4/IL-13 receptor antagonist (dupilumab) or oral JAK inhibitors for moderate-to-severe disease.",
        "prevention": "Short daily lukewarm baths followed immediately ('soak and seal') by emollient moisturizer application, wearing soft cotton garments, maintaining humidified indoor air, avoiding harsh soaps and detergents, and trimming fingernails.",
        "content": "Atopic dermatitis is a chronic, relapsing, pruritic inflammatory dermatosis that represents the initial manifestation of the 'atopic march' (often preceding allergic rhinitis, food allergy, and asthma in children). Defective epidermal barrier integrity permits heightened transepidermal water loss and enhanced penetration of environmental allergens and irritants. Pruritus impairs sleep quality and daytime concentration. Secondary cutaneous infections, particularly impetiginization by S. aureus or eczema herpeticum caused by herpes simplex virus, require prompt antimicrobial intervention.",
        "source": "American Academy of Dermatology & NIH MedlinePlus"
    },
    {
        "document_id": "DOC_059",
        "title": "Drug Hypersensitivity and Penicillin Allergy: True IgE Allergy versus Adverse Drug Reaction",
        "category": "Allergy & Immunology",
        "disease": "Drug Allergy",
        "symptoms": "Immediate reactions (within 1 hour): urticaria, angioedema, bronchospasm, anaphylactic shock. Delayed reactions (days to weeks): morbilliform maculopapular exanthem, serum sickness, drug reaction with eosinophilia and systemic symptoms (DRESS), Stevens-Johnson syndrome (SJS).",
        "causes": "Immunological reaction against low-molecular-weight pharmacological agents acting as haptens (covalently binding to carrier serum proteins to form complete immunogens); penicillins, cephalosporins, sulfonamides, and anticonvulsants are common culprits.",
        "treatment": "Immediate and permanent discontinuation of the offending pharmaceutical agent; acute treatment of anaphylaxis with epinephrine; systemic corticosteroids and antihistamines for symptomatic relief; graded drug desensitization protocols when essential alternative antibiotics are unavailable.",
        "prevention": "Documenting drug allergies with precise clinical descriptions in medical records, avoiding cross-reactive compound classes, performing penicillin skin testing and supervised oral challenges to delabel false penicillin allergies.",
        "content": "True drug allergies are adverse drug reactions mediated through immunological mechanisms (Gell and Coombs classifications types I through IV). Notably, approximately 90% of individuals labeled as having a 'penicillin allergy' are found not to be genuinely allergic upon formal allergist evaluation with skin testing and oral amoxicillin challenge. Over-reporting penicillin allergy leads to the inappropriate utilization of broad-spectrum second-line antibiotics, elevating healthcare costs, treatment failures, and antimicrobial resistance rates (e.g., Clostridioides difficile).",
        "source": "CDC & American College of Allergy, Asthma & Immunology"
    },
    {
        "document_id": "DOC_060",
        "title": "Peanut and Food Allergies: Sensitization, Epicutaneous Immunotherapy, and Oral Tolerance Induction",
        "category": "Allergy & Immunology",
        "disease": "Food Allergy",
        "symptoms": "Tingling or itching in the mouth, perioral urticaria, abdominal cramping, vomiting, diarrhea, acute wheezing, stridor, hypotension, dizziness, anaphylaxis occurring within minutes of food ingestion.",
        "causes": "IgE-mediated immune response to food allergen proteins (e.g., peanut storage proteins Ara h 1, Ara h 2, Ara h 6; milk caseins; egg ovalbumin). Failure to establish or maintain oral mucosal immune tolerance.",
        "treatment": "Prompt intramuscular epinephrine for anaphylactic manifestations; oral peanut immunotherapy (Palforzia) for desensitization in pediatric patients; strict dietary avoidance of implicated foods.",
        "prevention": "Early dietary introduction of peanut-containing foods around 4 to 6 months of age in infants with severe eczema or egg allergy (based on the LEAP study recommendations) to promote mucosal tolerance, meticulous food label reading.",
        "content": "Food allergy is an adverse immunological response arising reproducibly upon ingestion of specific dietary proteins. The 'big nine' food allergens comprise milk, eggs, peanuts, tree nuts, fish, crustacean shellfish, wheat, soy, and sesame. Diagnosis combines clinical history with skin prick testing and serum allergen-specific IgE quantification; the double-blind placebo-controlled oral food challenge (DBPCFC) remains the definitive diagnostic gold standard. Strict cross-contact prevention in school and restaurant settings is essential to protect sensitized individuals.",
        "source": "NIH National Institute of Allergy and Infectious Diseases & CDC"
    },

    # 12. ENDOCRINE & METABOLIC (EXPANDED)
    {
        "document_id": "DOC_061",
        "title": "Hypothyroidism and Hashimoto's Thyroiditis: Autoimmune Destruction and Levothyroxine Replacement",
        "category": "Endocrinology",
        "disease": "Hypothyroidism",
        "symptoms": "Cold intolerance, persistent fatigue, unexplained weight gain, constipation, dry coarse skin, brittle hair, periorbital puffiness, hoarse voice, bradycardia, menorrhagia, memory fog, depressed mood.",
        "causes": "Hashimoto's thyroiditis (chronic lymphocytic thyroiditis characterized by anti-TPO and anti-thyroglobulin antibodies), iatrogenic (radioactive iodine ablation, thyroidectomy), severe iodine deficiency, or secondary pituitary insufficiency.",
        "treatment": "Oral levothyroxine sodium monotherapy taken on an empty stomach 30-60 minutes before breakfast with water; dosage titrated every 6-8 weeks based on serum Thyroid-Stimulating Hormone (TSH) levels.",
        "prevention": "Universal salt iodization to eradicate endemic goiter; routine TSH screening during pregnancy and in patients with other autoimmune diseases (type 1 diabetes, vitiligo).",
        "content": "Hypothyroidism is a systemic endocrine disorder caused by insufficient synthesis and secretion of thyroid hormones (thyroxine [T4] and triiodothyronine [T3]). Primary hypothyroidism features elevated serum TSH and decreased free T4. If left untreated, chronic severe hypothyroidism can culminate in myxedema coma—a rare, life-threatening crisis marked by hypothermia, severe hypoventilation, bradycardia, pericardial effusion, and altered sensorium that requires prompt intravenous levothyroxine and stress-dose corticosteroids.",
        "source": "American Thyroid Association & NIH MedlinePlus"
    },
    {
        "document_id": "DOC_062",
        "title": "Hyperthyroidism and Graves' Disease: TSH Receptor Antibodies, Thyrotoxicosis, and Antithyroid Drugs",
        "category": "Endocrinology",
        "disease": "Hyperthyroidism",
        "symptoms": "Heat intolerance, unexplained weight loss despite increased appetite, palpitations, sinus tachycardia, atrial fibrillation, fine hand tremor, frequent bowel movements, moist warm skin, insomnia, Graves' ophthalmopathy (exophthalmos, proptosis).",
        "causes": "Graves' disease (autoantibodies stimulating the TSH receptor [TRAb]), toxic multinodular goiter (Plummer disease), autonomous toxic thyroid adenoma, subacute granulomatous thyroiditis, or excessive exogenous thyroid hormone ingestion.",
        "treatment": "Thionamide antithyroid medications (methimazole, propylthiouracil in first trimester of pregnancy); beta-adrenergic blockers (propranolol, atenolol) for acute adrenergic symptom control; definitive therapy with radioactive iodine ablation (I-131) or total thyroidectomy.",
        "prevention": "Avoiding excessive pharmacological iodine loads in predisposed individuals; smoking cessation strongly reduces the development and progression of Graves' orbitopathy.",
        "content": "Hyperthyroidism refers to inappropriate excess synthesis and secretion of thyroid hormones by an overactive thyroid gland, resulting in hypermetabolic thyrotoxicosis. Laboratory testing demonstrates suppressed serum TSH (<0.01 mIU/L) with elevated free T4 and/or free T3. Thyroid storm is a hyperthyroid emergency precipitated by acute stress, surgery, or infection, manifesting as extreme hyperpyrexia, severe tachycardia, delirium, and high-output congestive heart failure that demands intensive multimodality therapy.",
        "source": "American Thyroid Association & Mayo Clinic"
    },
    {
        "document_id": "DOC_063",
        "title": "Metabolic Syndrome: Diagnostic Criteria, Cardiovascular Risk, and Insulin Resistance",
        "category": "Endocrinology",
        "disease": "Metabolic Syndrome",
        "symptoms": "Typically asymptomatic; prominent physical signs include central/abdominal obesity (waist circumference >102 cm in men, >88 cm in women), acanthosis nigricans (hyperpigmented velvety cutaneous plaques in neck and axillae), elevated blood pressure.",
        "causes": "Underlying peripheral and hepatic insulin resistance compounded by visceral adiposity, high-calorie atherogenic diet, physical inactivity, neurohormonal activation, and genetic susceptibility.",
        "treatment": "Comprehensive lifestyle intervention: 7-10% sustained weight reduction, Mediterranean or DASH dietary pattern, >=150 minutes weekly of moderate-intensity aerobic exercise; pharmacotherapy targeting individual components: statins, antihypertensives, metformin, SGLT2 inhibitors.",
        "prevention": "Maintaining a healthy body weight throughout adulthood, engaging in daily physical activities, minimizing consumption of refined carbohydrates and trans fats, and routine metabolic screening.",
        "content": "Metabolic syndrome (Syndrome X) is a clustering of interconnected physiological, biochemical, and metabolic factors that directly confer a fivefold elevation in type 2 diabetes risk and a twofold increase in cardiovascular disease mortality. According to ATP III and IDF consensus criteria, diagnosis requires any three of five features: central adiposity, elevated fasting triglycerides (>=150 mg/dL), reduced HDL cholesterol (<40 mg/dL in men, <50 mg/dL in women), elevated blood pressure (>=130/85 mmHg), and elevated fasting blood glucose (>=100 mg/dL).",
        "source": "American Heart Association & NIH MedlinePlus"
    },
    {
        "document_id": "DOC_064",
        "title": "Obesity: Adiposity Pathophysiology, BMI Classification, and GLP-1 Receptor Agonists",
        "category": "Endocrinology",
        "disease": "Obesity",
        "symptoms": "Excessive accumulation of body fat; exertional dyspnea, obstructive sleep apnea, joint arthralgia, reduced functional mobility, chronic fatigue, gastroesophageal reflux, emotional distress.",
        "causes": "Chronic positive energy balance (caloric intake exceeding expenditure), genetic predisposition influencing hypothalamic satiety circuits (leptin-melanocortin pathway), obesogenic environments, sedentary behavior, endocrine-disrupting chemicals, and sleep deprivation.",
        "treatment": "Multi-component lifestyle therapy (diet, exercise, behavioral counseling); anti-obesity medications: GLP-1/GIP receptor agonists (semaglutide, tirzepatide), phentermine-topiramate, bupropion-naltrexone; metabolic bariatric surgery (Roux-en-Y gastric bypass, sleeve gastrectomy) for BMI >=35 or >=30 with major comorbidities.",
        "prevention": "Public health initiatives supporting physical activity infrastructure, promoting whole-food dietary patterns, restricting marketing of ultra-processed foods to children, and early childhood growth monitoring.",
        "content": "Obesity is a complex, chronic, relapsing neurobehavioral disease defined by abnormal or excessive adiposity that impairs health. It is categorized by Body Mass Index (BMI): Class 1 (30.0-34.9 kg/m²), Class 2 (35.0-39.9 kg/m²), and Class 3 (>=40.0 kg/m²). Visceral adipose tissue functions as an active endocrine organ, secreting pro-inflammatory adipokines (TNF-alpha, IL-6) that trigger systemic endothelial dysfunction, non-alcoholic fatty liver disease, hypertension, and numerous malignancies.",
        "source": "The Lancet Commission on Obesity & WHO Guidelines"
    },
    {
        "document_id": "DOC_065",
        "title": "Cushing's Syndrome: Hypercortisolemia, Pituitary ACTH Adenoma, and Dexamethasone Suppression",
        "category": "Endocrinology",
        "disease": "Cushing Syndrome",
        "symptoms": "Centripetal obesity, rounded 'moon' face, dorsocervical fat pad ('buffalo hump'), wide violaceous abdominal striae, proximal muscle weakness, thin fragile skin with easy bruising, hirsutism, secondary hypertension, glucose intolerance.",
        "causes": "Iatrogenic exogenous corticosteroid administration (most common); endogenous causes include ACTH-secreting pituitary adenoma (Cushing disease, ~70% of endogenous cases), ectopic ACTH production (small cell lung carcinoma), and autonomous cortisol-secreting adrenocortical adenomas.",
        "treatment": "Gradual taper of exogenous steroids; transsphenoidal surgical resection for pituitary microadenomas; laparoscopic unilateral adrenalectomy for adrenal tumors; medical adrenal-blocking therapy (ketoconazole, metyrapone, osilodrostat).",
        "prevention": "Prescribing the lowest effective dose of exogenous corticosteroids for the shortest duration; clinical vigilance when high-dose systemic steroid regimens are required.",
        "content": "Cushing's syndrome denotes the clinical constellation resulting from prolonged exposure to pathological levels of free glucocorticoids. Initial screening tests include 24-hour urinary free cortisol (UFC), late-night salivary cortisol, and the overnight 1-mg low-dose dexamethasone suppression test (DST). Once hypercortisolemia is established, plasma ACTH levels differentiate ACTH-dependent from ACTH-independent causes, followed by pituitary MRI, high-dose dexamethasone suppression testing, or bilateral inferior petrosal sinus sampling (IPSS).",
        "source": "The Endocrine Society & NIH MedlinePlus"
    },

    # 13. ADDITIONAL GASTROINTESTINAL & HEPATIC
    {
        "document_id": "DOC_066",
        "title": "Celiac Disease: Gluten-Sensitive Enteropathy, HLA-DQ2/DQ8, and Villous Atrophy",
        "category": "Gastroenterology",
        "disease": "Celiac Disease",
        "symptoms": "Chronic diarrhea, steatorrhea (pale, bulky, malodorous fatty stools), abdominal distension, flatulence, weight loss, iron deficiency anemia resistant to oral iron, dermatitis herpetiformis (pruritic blistering skin rash), growth failure in children.",
        "causes": "Immune-mediated enteropathy triggered by dietary ingestion of gluten peptides (gliadin found in wheat, rye, and barley) in genetically susceptible individuals carrying HLA-DQ2 or HLA-DQ8.",
        "treatment": "Strict, lifelong adherence to a 100% gluten-free diet (GFD); consultation with a specialized dietitian; correction of secondary micronutrient deficiencies (iron, calcium, vitamin D, B12); systemic dapsone for dermatitis herpetiformis.",
        "prevention": "No established primary prevention; avoidance of all cross-contamination of food preparation surfaces and utensils is essential for secondary prevention of intestinal inflammation and lymphoma.",
        "content": "Celiac disease is a systemic autoimmune disorder characterized by mucosal inflammation, crypt hyperplasia, and progressive blunting and loss of intestinal villi (villous atrophy) in the duodenum and jejunum upon gluten exposure. Serological screening relies on IgA tissue transglutaminase antibodies (tTG-IgA) alongside total serum IgA quantification. Confirmation requires upper endoscopy with multiple duodenal biopsies classified according to the Marsh criteria. Adherence to a gluten-free diet restores mucosal architecture and reduces enteropathy-associated T-cell lymphoma (EATL) risk.",
        "source": "American College of Gastroenterology & Celiac Disease Foundation"
    },
    {
        "document_id": "DOC_067",
        "title": "Crohn's Disease: Transmural Granulomatous Ileocolitis and Biologic Anti-TNF Therapy",
        "category": "Gastroenterology",
        "disease": "Crohn's Disease",
        "symptoms": "Cramping right lower quadrant abdominal pain, chronic non-bloody diarrhea, low-grade fever, weight loss, anorexia, perianal fistulas and abscesses, oral aphthous ulcers, erythema nodosum.",
        "causes": "Inappropriate mucosal immune response to enteric commensal microbiota in genetically predisposed individuals (NOD2/CARD15 mutations), characterized by Th1/Th17 cell activation and transmural inflammation.",
        "treatment": "Induction of remission: systemic corticosteroids (budesonide, prednisone); maintenance therapy: immunomodulators (azathioprine, 6-mercaptopurine), biologic anti-TNF agents (infliximab, adalimumab), anti-IL12/23 (ustekinumab), anti-integrin (vedolizumab); surgical bowel-sparing resection for strictures or fistulas.",
        "prevention": "Tobacco smoking strongly increases the risk and severity of Crohn's disease and must be strictly avoided; maintaining nutrient-dense diets and routine colorectal cancer surveillance.",
        "content": "Crohn's disease is an idiopathic chronic inflammatory bowel disease capable of affecting any segment of the gastrointestinal tract from the mouth to the anus, with a predilection for the terminal ileum and cecum ('terminal ileitis'). Colonoscopy classically demonstrates discontinuous mucosal involvement ('skip lesions'), cobblestone mucosal appearance, and deep linear ulcerations. Histopathology reveals transmural inflammation with non-caseating granulomas. Complications include mechanical bowel obstruction from fibrostenotic strictures, enteroenteric fistulae, and intra-abdominal abscesses.",
        "source": "Crohn's & Colitis Foundation & NIH MedlinePlus"
    },
    {
        "document_id": "DOC_068",
        "title": "Ulcerative Colitis: Continuous Mucosal Proctocolitis and 5-Aminosalicylic Acid (5-ASA)",
        "category": "Gastroenterology",
        "disease": "Ulcerative Colitis",
        "symptoms": "Frequent small-volume bloody diarrhea with passage of mucus, tenesmus (painful urgency to defecate), crampy left lower quadrant abdominal pain, nocturnal defecation, fatigue, fever, weight loss in severe flares.",
        "causes": "Dysregulated mucosal immune response restricted to the colorectal mucosa, with genetic susceptibility, barrier dysfunction, and atypical Th2 response.",
        "treatment": "First-line for mild-to-moderate disease: 5-aminosalicylates (mesalamine, sulfasalazine) oral and topical rectal formulations; corticosteroids for acute flares; biologic agents (anti-TNF, vedolizumab) or JAK inhibitors (tofacitinib); curative restorative proctocolectomy with ileal pouch-anal anastomosis (IPAA) for medically refractory disease or dysplasia.",
        "prevention": "Lifelong maintenance medication adherence to prevent relapses; colonoscopic surveillance every 1-2 years beginning 8 years after symptom onset to detect colorectal dysplasia.",
        "content": "Ulcerative colitis (UC) is a chronic inflammatory condition characterized by continuous, confluent superficial mucosal inflammation initiating in the rectum (proctitis) and extending proximally into the colon to varying degrees (left-sided colitis or pancolitis). Flexible sigmoidoscopy reveals mucosal erythema, loss of normal vascular pattern, friability, and pseudopolyps. Toxic megacolon—a severe complication marked by acute non-obstructive colonic dilation (>6 cm on radiograph) accompanied by systemic toxicity—demands emergent medical and surgical intervention.",
        "source": "American College of Gastroenterology & NHS"
    },
    {
        "document_id": "DOC_069",
        "title": "Irritable Bowel Syndrome (IBS): Gut-Brain Axis, Rome IV Criteria, and Low-FODMAP Diet",
        "category": "Gastroenterology",
        "disease": "Irritable Bowel Syndrome",
        "symptoms": "Recurrent abdominal pain related to defecation, changes in stool frequency (diarrhea, constipation, or alternating), changes in stool consistency, abdominal bloating, sensation of incomplete evacuation.",
        "causes": "Disorder of gut-brain interaction (DGBI) involving visceral hypersensitivity, altered gastrointestinal motility, post-infectious subclinical mucosal inflammation, and psychosocial stress.",
        "treatment": "Dietary modification (trial of low-FODMAP diet under dietitian supervision); soluble fiber supplementation (psyllium); antispasmodics (hyoscyamine, dicyclomine); for IBS-D: rifaximin, alosetron, loperamide; for IBS-C: osmotic laxatives (polyethylene glycol), linaclotide, lubiprostone; neuromodulators (low-dose tricyclic antidepressants).",
        "prevention": "Stress management, cognitive behavioral therapy, regular physical exercise, avoiding known gas-producing dietary triggers, and maintaining regular bowel habits.",
        "content": "Irritable Bowel Syndrome (IBS) is a functional gastrointestinal disorder diagnosed via the Rome IV criteria: recurrent abdominal pain at least 1 day per week in the last 3 months, associated with two or more of: related to defecation, change in stool frequency, or change in stool form. Subtypes include IBS with predominant constipation (IBS-C), IBS with predominant diarrhea (IBS-D), mixed (IBS-M), and unclassified. Diagnosis requires absence of red flag 'alarm features' (unintentional weight loss, nocturnal symptoms, rectal bleeding, onset after age 50, anemia, family history of colorectal cancer).",
        "source": "Rome Foundation & NIH MedlinePlus"
    },
    {
        "document_id": "DOC_070",
        "title": "Acute Pancreatitis: Gallstones, Alcohol, Lipase Elevation, and Atlanta Classification",
        "category": "Gastroenterology",
        "disease": "Acute Pancreatitis",
        "symptoms": "Severe, sudden epigastric abdominal pain radiating straight through to the back, exacerbated by supine positioning and relieved by leaning forward; nausea, persistent vomiting, epigastric tenderness, tachycardia, fever.",
        "causes": "Biliary ductal obstruction by gallstones (~40-50%) and heavy alcohol consumption (~30-35%); other causes include severe hypertriglyceridemia (>1000 mg/dL), post-ERCP, hypercalcemia, and medications.",
        "treatment": "Early aggressive goal-directed intravenous fluid resuscitation (preferably lactated Ringer's solution); effective multimodal intravenous analgesia (opioids); early enteral nutrition (oral or nasojejunal) as tolerated; urgent ERCP within 24-48 hours if concurrent cholangitis or biliary obstruction is present; laparoscopic cholecystectomy during same index admission for gallstone pancreatitis.",
        "prevention": "Elective cholecystectomy following recovery from gallstone pancreatitis, permanent alcohol abstinence, and pharmacological reduction of severe hypertriglyceridemia (fibrates).",
        "content": "Acute pancreatitis involves acute non-bacterial enzymatic autodigestion of the pancreatic parenchyma triggered by premature intracellular activation of trypsinogen to trypsin within acinar cells. Diagnosis requires at least two of three criteria: typical severe epigastric abdominal pain, serum amylase or lipase elevated >=3 times upper limit of normal, and characteristic cross-sectional imaging findings (contrast-enhanced CT or MRI). The revised Atlanta classification stratifies severity into mild (no organ failure), moderately severe (transient organ failure <48 hours), and severe (persistent organ failure >48 hours).",
        "source": "American College of Gastroenterology & NIH MedlinePlus"
    },

    # 14. INFECTIOUS DISEASES & DERMATOLOGY (EXPANDED)
    {
        "document_id": "DOC_071",
        "title": "Herpes Zoster (Shingles): Varicella Zoster Virus Reactivation and Postherpetic Neuralgia",
        "category": "Infectious Diseases",
        "disease": "Herpes Zoster",
        "symptoms": "Unilateral dermatomal pain, burning, tingling, or hyperesthesia preceding an eruption of grouped erythematous papules and vesicles that do not cross the midline; postherpetic neuralgia (chronic neuropathic pain lasting >3 months).",
        "causes": "Reactivation of latent Varicella Zoster Virus (VZV) residing in dorsal root or cranial nerve ganglia following remote primary chickenpox infection, precipitated by waning cell-mediated immunity due to aging or immunosuppression.",
        "treatment": "Oral antivirals (valacyclovir, famciclovir, acyclovir) initiated within 72 hours of rash onset to accelerate lesion healing and decrease neuralgia risk; analgesics, gabapentin, or pregabalin for neuropathic pain.",
        "prevention": "Recombinant zoster vaccine (Shingrix), a two-dose non-live adjuvanted vaccine strongly recommended for all immunocompetent adults aged >=50 years and immunocompromised individuals >=19 years.",
        "content": "Herpes zoster (shingles) occurs when latent varicella zoster virus escapes immune surveillance within sensory neural ganglia and travels along the sensory nerve axon to the corresponding cutaneous dermatome. Complications include herpes zoster ophthalmicus (involvement of ophthalmic division V1 of trigeminal nerve, risking corneal ulceration and blindness), Ramsay Hunt syndrome (facial nerve VII and vestibulocochlear VIII involvement causing facial palsy and otic vesicles), and debilitating chronic postherpetic neuralgia (PHN).",
        "source": "CDC & Mayo Clinic"
    },
    {
        "document_id": "DOC_072",
        "title": "Psoriasis Vulgaris: Plaque Psoriasis, IL-23/IL-17 Axis, and Biologic Therapeutics",
        "category": "Dermatology",
        "disease": "Psoriasis",
        "symptoms": "Well-demarcated erythematous plaques covered with coarse silvery-white micaceous scales, prominent on extensor surfaces (elbows, knees, lumbosacral region, scalp), pruritus, nail pitting and onycholysis, positive Auspitz sign (pinpoint bleeding upon scale removal).",
        "causes": "Immune-mediated genetic dermatosis driven by abnormal crosstalk between epidermal keratinocytes and dendritic cells, causing hyperactivation of the IL-23/IL-17/TNF-alpha immune axis.",
        "treatment": "Topical therapy for mild disease: high-potency corticosteroids (clobetasol) combined with vitamin D analogs (calcipotriene); narrowband ultraviolet B (NB-UVB) phototherapy; systemic agents (methotrexate, apremilast); targeted biologics (anti-TNF, anti-IL-17, anti-IL-23) for moderate-to-severe disease.",
        "prevention": "Avoidance of known disease triggers (streptococcal pharyngitis, skin trauma [Koebner phenomenon], emotional stress, beta-blockers, lithium), maintaining skin hydration with emollients.",
        "content": "Psoriasis vulgaris is a chronic inflammatory papulosquamous skin disease characterized by rapid keratinocyte hyperproliferation and incomplete differentiation, reducing epidermal cell turnover from the normal 28 days to only 3-5 days. Approximately 20-30% of patients develop psoriatic arthritis, a potentially erosive inflammatory joint disorder. Psoriasis is strongly associated with cardiovascular comorbidities, obesity, and metabolic syndrome as a consequence of sustained systemic cytokine elevation.",
        "source": "National Psoriasis Foundation & NIH MedlinePlus"
    },
    {
        "document_id": "DOC_073",
        "title": "Urinary Tract Infection: Acute Cystitis, Pyelonephritis, and Uropathogenic Escherichia coli",
        "category": "Infectious Diseases",
        "disease": "Urinary Tract Infection",
        "symptoms": "Acute cystitis: dysuria (burning micturition), urinary frequency, urgency, suprapubic tenderness, foul-smelling or cloudy urine, hematuria. Pyelonephritis: flank pain, costovertebral angle tenderness, high fever, rigors, nausea, vomiting.",
        "causes": "Ascending bacterial infection from the perineum into the bladder and kidneys; Uropathogenic Escherichia coli (UPEC) causes >80% of uncomplicated cases; other pathogens include Klebsiella pneumoniae, Proteus mirabilis, and Staphylococcus saprophyticus.",
        "treatment": "First-line for uncomplicated cystitis: nitrofurantoin, trimethoprim-sulfamethoxazole, or fosfomycin trometamol; for acute pyelonephritis: oral or IV fluoroquinolones (ciprofloxacin) or third-generation cephalosporins (ceftriaxone); phenazopyridine for short-term symptomatic urinary analgesia.",
        "prevention": "Adequate daily water hydration, voiding immediately following sexual intercourse, wiping from front to back, avoiding spermicides, and topical vaginal estrogen in postmenopausal women with recurrent UTIs.",
        "content": "Urinary tract infections (UTIs) are among the most frequent bacterial infections, particularly in women due to a shorter anatomical urethra. While uncomplicated cystitis is confined to the superficial mucosal urothelium of the bladder, infection can ascend into the renal pelvis and parenchyma to cause acute pyelonephritis, which carries risk of bacteremia and urosepsis. Urinalysis demonstrating pyuria (>10 WBC/hpf), positive leukocyte esterase, and positive nitrite testing supports clinical diagnosis; urine culture directs targeted antibiotic selection.",
        "source": "Infectious Diseases Society of America (IDSA) & CDC"
    },
    {
        "document_id": "DOC_074",
        "title": "Bacterial Meningitis: Acute Meningococcal and Pneumococcal Central Nervous System Infection",
        "category": "Infectious Diseases",
        "disease": "Bacterial Meningitis",
        "symptoms": "Classic clinical triad: sudden high fever, severe headache, and nuchal rigidity (stiff neck); accompanied by photophobia, altered mental status, nausea, vomiting, positive Kernig and Brudzinski signs, petechial purpuric rash (Neisseria meningitidis).",
        "causes": "Hematogenous spread or direct extension of bacterial pathogens across the blood-brain barrier: Streptococcus pneumoniae, Neisseria meningitidis, Haemophilus influenzae type b, and Listeria monocytogenes (in elderly, neonates, and immunocompromised).",
        "treatment": "Immediate emergency empirical intravenous broad-spectrum bactericidal antibiotics (vancomycin plus third-generation cephalosporin ceftriaxone/cefotaxime, plus ampicillin if Listeria risk) co-administered with intravenous dexamethasone prior to or with the first antibiotic dose to reduce neurological morbidity.",
        "prevention": "Conjugate vaccines: meningococcal (MenACWY and MenB), pneumococcal (PCV15/20), and Hib vaccines; oral chemoprophylaxis (rifampin, ciprofloxacin, or ceftriaxone) for close household and intimate contacts of meningococcal disease cases.",
        "content": "Acute bacterial meningitis is a life-threatening medical emergency requiring urgent diagnosis and treatment within minutes. Bacterial lysis in the subarachnoid space triggers intense neutrophil infiltration, cerebral edema, heightened intracranial pressure, and decreased cerebral perfusion. Lumbar puncture reveals purulent CSF under elevated opening pressure, elevated polymorphonuclear pleocytosis (>1000/mm³), high protein (>100 mg/dL), and markedly depressed CSF-to-serum glucose ratio (<0.4). Delay in antibiotic administration significantly increases mortality and long-term neurosensory hearing loss.",
        "source": "CDC & WHO Guidelines"
    },
    {
        "document_id": "DOC_075",
        "title": "Infectious Mononucleosis: Epstein-Barr Virus, Heterophile Antibodies, and Splenomegaly",
        "category": "Infectious Diseases",
        "disease": "Infectious Mononucleosis",
        "symptoms": "Fever, severe sore throat with exudative pharyngotonsillitis, tender posterior cervical lymphadenopathy, profound prolonged fatigue, splenomegaly, palatal petechiae, hepatomegaly.",
        "causes": "Primary infection with Epstein-Barr Virus (EBV, Human Herpesvirus 4), transmitted through oral secretions ('kissing disease'); selectively infects B-lymphocytes via the CD21 receptor, inducing vigorous CD8+ cytotoxic T-cell proliferative response.",
        "treatment": "Supportive therapy: adequate hydration, antipyretics and analgesics (acetaminophen, NSAIDs), salt water gargles, rest; systemic corticosteroids are indicated only for severe airway obstruction due to tonsillar hypertrophy, hemolytic anemia, or severe thrombocytopenia; avoid amoxicillin/ampicillin which triggers maculopapular rash.",
        "prevention": "Avoiding sharing beverages, food utensils, toothbrushes, and kissing with individuals diagnosed with acute mononucleosis; strict cessation of contact sports for >=3-4 weeks to prevent catastrophic splenic rupture.",
        "content": "Infectious mononucleosis is an acute clinical syndrome most frequently encountered in adolescents and young adults. Peripheral blood film demonstrates marked atypical lymphocytosis (>=10% reactive atypical CD8+ T lymphocytes). Diagnosis is confirmed using rapid heterophile antibody testing (Monospot assay) or EBV-specific viral capsid antigen (VCA IgM/IgG) serology. Because the spleen becomes congested and fragile, acute blunt trauma carries risk of splenic rupture, necessitating mandatory athletic restriction until splenic normalization.",
        "source": "CDC & NIH MedlinePlus"
    },

    # 15. RESPIRATORY & PULMONARY (EXPANDED)
    {
        "document_id": "DOC_076",
        "title": "Pulmonary Embolism: Deep Vein Thrombosis, Wells Criteria, and Anticoagulation",
        "category": "Cardiovascular & Respiratory",
        "disease": "Pulmonary Embolism",
        "symptoms": "Sudden onset of dyspnea, pleuritic chest pain, tachypnea, tachycardia, hemoptysis, syncope, unilateral lower extremity swelling and tenderness (DVT); severe massive embolism causes acute circulatory collapse.",
        "causes": "Thromboembolism originating from proximal deep veins of the lower extremities (iliac, femoral, popliteal) embolizing through the right heart to occlude the pulmonary arterial bed. Risk factors (Virchow's triad: stasis, hypercoagulability, endothelial injury) include major surgery, trauma, immobilization, malignancy, oral contraceptives.",
        "treatment": "Direct oral anticoagulants (DOACs: apixaban, rivaroxaban) or low-molecular-weight heparin (enoxaparin) transitioned to warfarin; systemic thrombolytic therapy (alteplase) or catheter-directed embolectomy for hemodynamically unstable massive PE with systemic hypotension.",
        "prevention": "Venous thromboembolism (VTE) prophylaxis in hospitalized and postoperative patients with mechanical compression devices and pharmacologic heparin; early postoperative ambulation; avoiding prolonged immobility on long flights.",
        "content": "Pulmonary embolism (PE) is the third most common cause of cardiovascular death globally. Obstruction of pulmonary arterial blood flow produces dead space ventilation, ventilation-perfusion mismatch, and acute right ventricular afterload overload. The Wells score or Geneva score stratifies pretest clinical probability. In low-to-intermediate risk patients, a negative high-sensitivity D-dimer safely excludes PE, while computed tomography pulmonary angiography (CTPA) represents the definitive confirmatory imaging standard.",
        "source": "American Heart Association & European Society of Cardiology"
    },
    {
        "document_id": "DOC_077",
        "title": "Obstructive Sleep Apnea: Nocturnal Pharyngeal Collapse, Polysomnography, and CPAP",
        "category": "Respiratory",
        "disease": "Sleep Apnea",
        "symptoms": "Loud chronic snoring, witnessed nocturnal breathing pauses or choking episodes, restless sleep, morning headache, excessive daytime sleepiness (Epworth Sleepiness Scale >10), difficulty concentrating, irritability.",
        "causes": "Recurrent functional collapse of the upper pharyngeal airway during sleep due to loss of motor dilator muscle tone in the setting of anatomical narrowing (pharyngeal fat deposition in obesity, retrognathia, enlarged tonsils/adenoids).",
        "treatment": "Continuous Positive Airway Pressure (CPAP) as first-line therapy providing pneumatic splinting to upper airway; custom oral mandibular advancement devices; positional therapy; weight loss through lifestyle or bariatric surgery; surgical uvulopalatopharyngoplasty (UPPP).",
        "prevention": "Weight reduction, avoiding alcohol and sedative medications prior to bedtime, cessation of smoking, and treating nasal congestion.",
        "content": "Obstructive sleep apnea (OSA) is characterized by repetitive complete (apnea) or partial (hypopnea) upper airway obstruction during sleep, resulting in cyclical arterial oxygen desaturation, surges in sympathetic activity, and recurrent electroencephalographic arousals. Diagnosis is confirmed through overnight polysomnography establishing an Apnea-Hypopnea Index (AHI >=5 events/hour with symptoms, or >=15 events/hour). Untreated severe OSA substantially amplifies long-term risks of resistant hypertension, atrial fibrillation, coronary artery disease, stroke, and motor vehicle accidents.",
        "source": "American Academy of Sleep Medicine & NIH MedlinePlus"
    },
    {
        "document_id": "DOC_078",
        "title": "Idiopathic Pulmonary Fibrosis: Chronic Progressive Fibrosing Interstitial Pneumonia and Antifibrotics",
        "category": "Respiratory",
        "disease": "Pulmonary Fibrosis",
        "symptoms": "Progressive, unremitting exertional dyspnea, chronic dry non-productive cough, bilateral fine inspiratory 'Velcro-like' crackles on lung auscultation, digital clubbing of fingers and toes.",
        "causes": "Unknown etiology; repetitive subclinical alveolar epithelial microinjuries followed by aberrant wound repair, fibroblast proliferation, and exuberant extracellular matrix deposition in genetically susceptible aging adults.",
        "treatment": "Antifibrotic pharmacotherapy with pirfenidone or nintedanib to retard decline in forced vital capacity (FVC); supplemental oxygen for exertional or resting hypoxemia; pulmonary rehabilitation; lung transplantation evaluation in eligible candidates.",
        "prevention": "Tobacco smoking cessation, avoiding occupational and environmental inhalation exposures (silica, metal dusts, coal, biomass smoke).",
        "content": "Idiopathic Pulmonary Fibrosis (IPF) is a chronic, progressive, irreversible fibrosing interstitial lung disease of unknown etiology occurring primarily in adults older than 60 years. High-resolution computed tomography (HRCT) of the chest reveals the characteristic usual interstitial pneumonia (UIP) pattern: peripheral, subpleural, basal-predominant reticular opacities, traction bronchiectasis, and subpleural 'honeycombing' without prominent ground-glass opacities. IPF carries a poor prognosis with median survival of 3 to 5 years from diagnosis without treatment.",
        "source": "American Thoracic Society & NIH National Heart, Lung, and Blood Institute"
    },
    {
        "document_id": "DOC_079",
        "title": "Pleural Effusion: Transudative versus Exudative Effusions and Light's Criteria",
        "category": "Respiratory",
        "disease": "Pleural Effusion",
        "symptoms": "Dyspnea on exertion, pleuritic chest pain aggravated by deep inspiration or coughing, dry cough; physical examination demonstrates dullness to percussion, decreased tactile fremitus, and diminished or absent breath sounds over the effusion.",
        "causes": "Transudative effusions: congestive heart failure, cirrhosis with hepatic hydrothorax, nephrotic syndrome, severe hypoalbuminemia; Exudative effusions: parapneumonic bacterial infection, empyema, malignant neoplasms (lung, breast, lymphoma), pulmonary embolism, tuberculosis, rheumatoid arthritis.",
        "treatment": "Diagnostic and therapeutic thoracentesis; treating underlying cause (diuretics for heart failure, antibiotics and tube thoracostomy drainage for complicated parapneumonic effusions/empyema, indwelling pleural catheter or chemical pleurodesis with talc for malignant effusions).",
        "prevention": "Effective clinical management of chronic underlying heart failure, liver cirrhosis, and prompt antibiotic treatment of acute community-acquired pneumonia to prevent parapneumonic fluid collection.",
        "content": "Pleural effusion is the pathological accumulation of fluid within the pleural cavity between the visceral and parietal pleurae. Light's criteria classify pleural aspirates: an effusion is exudative if pleural fluid protein/serum protein ratio >0.5, pleural fluid LDH/serum LDH ratio >0.6, or pleural fluid LDH > two-thirds upper normal limit of serum LDH. Transudates arise from imbalances in systemic hydrostatic or oncotic pressures, whereas exudates reflect local capillary hyperpermeability and pleural inflammation.",
        "source": "American Thoracic Society & Mayo Clinic"
    },
    {
        "document_id": "DOC_080",
        "title": "Bronchiectasis: Irreversible Bronchial Dilation, Impaired Mucociliary Clearance, and Macrolides",
        "category": "Respiratory",
        "disease": "Bronchiectasis",
        "symptoms": "Chronic daily productive cough with copious purulent or mucopurulent sputum, recurrent respiratory tract infections, dyspnea, wheezing, fatigue, hemoptysis, digital clubbing.",
        "causes": "Cycle of recurrent bacterial infection and chronic bronchial wall inflammation resulting in destruction of muscular and elastic components of bronchial walls; etiologies include cystic fibrosis, primary ciliary dyskinesia, post-infectious (childhood measles/pertussis/severe pneumonia), allergic bronchopulmonary aspergillosis (ABPA), and hypogammaglobulinemia.",
        "treatment": "Airway clearance techniques (chest physiotherapy, oscillatory positive expiratory pressure devices); inhaled hypertonic saline; targeted antimicrobials for acute exacerbations; long-term oral macrolide prophylaxis (azithromycin) for anti-inflammatory effects in frequent exacerbators; inhaled bronchodilators.",
        "prevention": "Childhood vaccination against pertussis and measles, prompt antibiotic treatment of acute lower respiratory infections, and early diagnosis and specialized management of cystic fibrosis.",
        "content": "Bronchiectasis is a chronic pulmonary condition marked by irreversible, abnormal dilation of the bronchi and bronchioles accompanied by impaired mucociliary clearance. Stagnant mucus promotes persistent bacterial colonization, particularly by Pseudomonas aeruginosa and Haemophilus influenzae. High-Resolution CT (HRCT) of the chest is the gold standard imaging investigation, demonstrating the 'signet ring sign' where the internal diameter of the bronchus exceeds that of the adjacent bronchial artery, alongside bronchial wall thickening and lack of normal peripheral tapering.",
        "source": "British Thoracic Society & NIH MedlinePlus"
    },

    # 16. ADDITIONAL CARDIOVASCULAR CONDITIONS
    {
        "document_id": "DOC_081",
        "title": "Atrial Fibrillation: Supraventricular Tachyarrhythmia, Stroke Risk, and Anticoagulation",
        "category": "Cardiovascular",
        "disease": "Atrial Fibrillation",
        "symptoms": "Irregularly irregular heartbeat/pulse, palpitations, fatigue, lightheadedness, exertional dyspnea, chest discomfort, syncope; up to 30% of patients are completely asymptomatic.",
        "causes": "Ectopic electrical foci predominantly originating in the muscular sleeves of the pulmonary veins, perpetuated by structural and electrical atrial remodeling. Risk factors include hypertension, valvular heart disease, aging, coronary disease, obesity, sleep apnea, and alcohol abuse ('holiday heart').",
        "treatment": "Stroke thromboembolism prevention using direct oral anticoagulants (DOACs: apixaban, rivaroxaban, dabigatran, edoxaban); rate control using beta-blockers, diltiazem, or verapamil; rhythm control via antiarrhythmic drugs (flecainide, amiodarone) or direct-current cardioversion; catheter ablation of pulmonary vein triggers.",
        "prevention": "Aggressive blood pressure control, weight management, CPAP therapy for sleep apnea, moderating alcohol consumption, and regular screening with pulse palpation or wearable ECG sensors.",
        "content": "Atrial fibrillation (AF) is the most prevalent sustained cardiac arrhythmia in adults, characterized by chaotic, disorganized atrial electrical activation without coordinated atrial mechanical contraction. Loss of atrial kick and blood stasis within the left atrial appendage (LAA) substantially accelerates intracardiac thrombus formation, increasing ischemic stroke risk fivefold. Stroke risk is systematically quantified using the CHA2DS2-VASc scoring system to guide oral anticoagulation decisions.",
        "source": "American Heart Association & European Heart Rhythm Association"
    },
    {
        "document_id": "DOC_082",
        "title": "Infective Endocarditis: Endothelial Vegetations, Duke Criteria, and Bactericidal Therapy",
        "category": "Cardiovascular",
        "disease": "Infective Endocarditis",
        "symptoms": "Unexplained persistent fever, chills, new or changing heart murmur, anorexia, night sweats, splinter hemorrhages in nail beds, Osler nodes (painful erythematous nodules on pads of fingers/toes), Janeway lesions (nontender macular lesions on palms/soles), Roth spots on fundoscopy.",
        "causes": "Microbial colonization of damaged valvular or mural endocardium, primarily caused by Staphylococcus aureus, viridans group Streptococci, Enterococci, and HACEK organisms; bacteremia induced by dental procedures, intravenous drug use, or indwelling intravenous lines.",
        "treatment": "Prolonged (4-6 weeks) intravenous bactericidal antibiotic therapy tailored to identified blood-culture organisms and minimum inhibitory concentrations (MICs); urgent valve repair or replacement surgery for heart failure, uncontrolled infection, or large mobile vegetations.",
        "prevention": "Prophylactic oral antibiotics (amoxicillin) prior to invasive dental procedures strictly in high-risk patients (prosthetic heart valves, previous infective endocarditis, unrepaired cyanotic congenital heart disease), meticulous oral hygiene, avoiding non-sterile injection practices.",
        "content": "Infective endocarditis (IE) involves microbial infection of the native or prosthetic heart valves and adjacent endocardial structures, forming friable vegetations composed of platelets, fibrin, microorganisms, and inflammatory cells. Embolization of vegetations produces metastatic abscesses, mycotic aneurysms, and ischemic strokes. Diagnosis is formulated using the Modified Duke Criteria, which integrate major criteria (persistently positive blood cultures for typical organisms and echocardiographic evidence of valvular vegetation or abscess) with minor clinical risk factors.",
        "source": "American Heart Association & European Society of Cardiology"
    },
    {
        "document_id": "DOC_083",
        "title": "Aortic Stenosis: Calcific Valvular Degeneration, Syncope, and TAVR Procedures",
        "category": "Cardiovascular",
        "disease": "Aortic Stenosis",
        "symptoms": "Classic symptom triad: exertional dyspnea (heart failure), exertional angina pectoris, and exertional syncope; harsh crescendo-decrescendo systolic ejection murmur radiating to carotids, parvus et tardus pulse (weak and delayed carotid upstroke).",
        "causes": "Age-related calcific degeneration of a normal trileaflet valve (predominant in elderly >70 years) or accelerated calcification of a congenitally bicuspid aortic valve (presenting earlier at 50-65 years); rheumatic heart disease in developing nations.",
        "treatment": "Definitive intervention upon symptom onset or severe left ventricular systolic dysfunction (LVEF <50%): Transcatheter Aortic Valve Replacement (TAVR) or Surgical Aortic Valve Replacement (SAVR); medical therapy provides only temporary palliative bridge support.",
        "prevention": "Managing cardiovascular risk factors (hypertension, smoking, hyperlipidemia), though no medical therapy has proven capable of arresting valvular calcific progression once initiated.",
        "content": "Aortic stenosis (AS) is the most common primary valvular heart disease requiring intervention in developed nations. Progressive fibrous thickening and calcification restrict aortic valve leaflet mobility, elevating left ventricular afterload and precipitating concentric left ventricular hypertrophy. Transthoracic echocardiography establishes severity: severe AS is defined by an aortic valve area <=1.0 cm², mean transvalvular gradient >=40 mmHg, or peak aortic jet velocity >=4.0 m/s. Once cardinal symptoms emerge, mortality climbs precipitously without prompt valve replacement.",
        "source": "American College of Cardiology & Mayo Clinic"
    },
    {
        "document_id": "DOC_084",
        "title": "Acute Pericarditis: Pericardial Friction Rub, PR Depression, and Colchicine",
        "category": "Cardiovascular",
        "disease": "Pericarditis",
        "symptoms": "Sharp, pleuritic retrosternal chest pain aggravated by deep inspiration, coughing, or lying supine, characteristically relieved by sitting up and leaning forward; pericardial friction rub on auscultation, low-grade fever.",
        "causes": "Most cases are idiopathic or presumed viral (Coxsackievirus, echovirus, influenza, EBV, SARS-CoV-2); non-viral causes include post-myocardial infarction (Dressler syndrome), connective tissue autoimmune diseases (SLE, RA), uremia, tuberculosis, and neoplastic metastases.",
        "treatment": "First-line combination therapy: high-dose NSAIDs (aspirin, ibuprofen, or indomethacin) plus colchicine for 3 months to prevent recurrences; systemic corticosteroids reserved for NSAID-refractory or autoimmune cases; pericardiocentesis for cardiac tamponade.",
        "prevention": "Adherence to full 3-month course of colchicine during the initial acute pericarditis episode significantly reduces the recurrence rate; avoiding strenuous physical exertion during the acute phase until symptoms and biomarkers normalize.",
        "content": "Acute pericarditis is an inflammatory disorder of the pericardial sac surrounding the heart. Diagnostic criteria require at least two of the following: characteristic positional pleuritic chest pain; auscultatory pericardial friction rub; widespread concavity-upward ST-segment elevation with PR-segment depression on 12-lead ECG; and new or worsening pericardial effusion on echocardiography. The major acute complication is cardiac tamponade, wherein fluid accumulation produces elevated intrapericardial pressure, jugular venous distension, hypotension, and pulsus paradoxus.",
        "source": "European Society of Cardiology & NIH MedlinePlus"
    },
    {
        "document_id": "DOC_085",
        "title": "Deep Vein Thrombosis: Lower Extremity Thrombus, D-dimer, and Compression Ultrasonography",
        "category": "Cardiovascular",
        "disease": "Deep Vein Thrombosis",
        "symptoms": "Unilateral lower extremity pain, erythema, warm skin, tenderness along venous trajectory, and pitting edema; calf circumference discrepancy >3 cm compared to asymptomatic leg.",
        "causes": "Venous thrombosis within deep veins (popliteal, femoral, iliac) triggered by elements of Virchow's triad: venous stasis (bed rest, long flights, cast immobilization), endothelial vascular injury (surgery, trauma, catheterization), and hypercoagulability (Factor V Leiden, malignancy, estrogen therapy).",
        "treatment": "Anticoagulation: Direct oral anticoagulants (apixaban, rivaroxaban) or LMWH bridging to warfarin for minimum 3 months; catheter-directed pharmacomechanical thrombolysis for extensive proximal phlegmasia cerulea dolens; inferior vena cava (IVC) filter in patients with contraindications to anticoagulation.",
        "prevention": "Mechanical prophylaxis with graduated compression stockings and intermittent pneumatic compression devices in surgical patients; pharmacologic thromboprophylaxis with low-dose heparin/LMWH; frequent ambulation during travel.",
        "content": "Deep vein thrombosis (DVT) represents the venous phase of venous thromboembolism. Without timely therapeutic intervention, fragments of lower extremity thrombi frequently detach and embolize through the inferior vena cava and right cardiac chambers to occlude the pulmonary circulation, causing potentially fatal pulmonary embolism. Compression duplex ultrasonography of the lower extremity veins—evaluating lack of venous luminal compressibility under probe pressure—is the primary diagnostic gold standard.",
        "source": "CDC & American Heart Association"
    },

    # 17. ADDITIONAL NEUROLOGICAL & PSYCHIATRIC
    {
        "document_id": "DOC_086",
        "title": "Multiple Sclerosis: Central Nervous System Demyelination, Oligoclonal Bands, and Disease-Modifying Therapies",
        "category": "Neurology",
        "disease": "Multiple Sclerosis",
        "symptoms": "Optic neuritis (monocular vision loss and painful eye movements), Lhermitte sign (electric-shock sensation down spine upon neck flexion), limb weakness, spasticity, sensory numbness/paresthesias, ataxia, bladder dysfunction, cognitive changes, heat sensitivity (Uhthoff phenomenon).",
        "causes": "Chronic autoimmune inflammatory demyelinating disease of the central nervous system, mediated by autoreactive myelin-specific CD4+ and CD8+ T cells and B cells destroying oligodendrocytes and myelin sheaths.",
        "treatment": "Acute relapses: high-dose intravenous methylprednisolone (1 g daily for 3-5 days) or plasma exchange; Disease-modifying therapies (DMTs): injectables (interferon-beta, glatiramer acetate), orals (fingolimod, teriflunomide, dimethyl fumarate), high-efficacy monoclonals (ocrelizumab, natalizumab, ofatumumab).",
        "prevention": "Adequate vitamin D levels during childhood and adolescence, smoking cessation, avoiding EBV infection where possible, and initiating early high-efficacy DMTs to prevent long-term disability progression.",
        "content": "Multiple sclerosis (MS) is the premier non-traumatic disabling neurological disease affecting young adults, typically diagnosed between ages 20 and 40. Clinical patterns include relapsing-remitting MS (RRMS, ~85% of cases), primary progressive MS (PPMS), and secondary progressive MS (SPMS). The McDonald criteria define diagnosis by establishing dissemination of inflammatory white-matter demyelinating lesions in both space and time on gadolinium-enhanced brain and spinal cord MRI, supported by detection of cerebrospinal fluid-restricted oligoclonal IgG bands.",
        "source": "National Multiple Sclerosis Society & NIH NINDS"
    },
    {
        "document_id": "DOC_087",
        "title": "Alzheimer's Disease: Amyloid Beta Plaques, Neurofibrillary Tangles, and Cholinesterase Inhibitors",
        "category": "Neurology",
        "disease": "Alzheimer's Disease",
        "symptoms": "Insidious onset of progressive short-term episodic memory loss, executive dysfunction, language impairment (anomia, aphasia), spatial disorientation, apraxia, neuropsychiatric symptoms (apathy, wandering, agnosia).",
        "causes": "Extracellular deposition of neurotoxic amyloid-beta (Abeta42) senile plaques and intracellular aggregation of hyperphosphorylated tau proteins forming neurofibrillary tangles, leading to synaptic dysfunction, neuronal loss, and profound cerebral atrophy.",
        "treatment": "Symptomatic pharmacotherapy: acetylcholinesterase inhibitors (donepezil, rivastigmine, galantamine) for mild-to-moderate dementia, NMDA receptor antagonist (memantine) for moderate-to-severe disease; disease-modifying anti-amyloid monoclonal antibodies (lecanemab, donanemab); structured cognitive stimulation.",
        "prevention": "Regular aerobic exercise, adherence to the Mediterranean-DASH diet (MIND diet), cognitive engagement and lifelong learning, managing cardiovascular risk factors (hypertension, diabetes), and hearing loss correction.",
        "content": "Alzheimer's disease is the predominant neurodegenerative etiology underlying dementia, accounting for 60-80% of clinical cases. Pathological alterations commence decades prior to manifest cognitive symptoms in the entorhinal cortex and hippocampus before disseminating neocortically. Diagnosis combines detailed neurocognitive testing, brain MRI (demonstrating medial temporal and hippocampal atrophy), and biomarker assays (cerebrospinal fluid or blood Abeta42/Abeta40 ratios and phosphorylated-tau-181/217).",
        "source": "Alzheimer's Association & NIH National Institute on Aging"
    },
    {
        "document_id": "DOC_088",
        "title": "Bell's Palsy: Idiopathic Peripheral Facial Nerve Paralysis and Corticosteroid Therapy",
        "category": "Neurology",
        "disease": "Bell's Palsy",
        "symptoms": "Abrupt onset of unilateral lower motor neuron facial weakness involving both the upper and lower face: inability to close the eye, eyebrow droop, flattening of nasolabial fold, mouth drooping, hyperacusis, impaired taste on anterior two-thirds of tongue.",
        "causes": "Edema and compression of the seventh cranial nerve (facial nerve) within the narrow Fallopian facial canal, presumed secondary to reactivation of latent Herpes Simplex Virus type 1 (HSV-1) or VZV.",
        "treatment": "Early oral corticosteroid therapy (prednisolone 50-60 mg daily for 10 days) initiated within 72 hours of symptom onset to reduce nerve edema; co-administration with oral antivirals (valacyclovir) in severe presentations; essential eye protection with lubricating ocular drops, daytime sunglasses, and nocturnal eye taping to prevent exposure keratitis.",
        "prevention": "No established primary prevention; diligent eye lubrication during the paralyzed period is mandatory to prevent corneal ulceration and permanent vision loss.",
        "content": "Bell's palsy is an acute, unilateral peripheral facial nerve neuropathy. A key clinical hallmark distinguishing Bell's palsy (lower motor neuron lesion) from central ischemic stroke (upper motor neuron lesion) is involvement of the forehead muscles: in Bell's palsy, forehead wrinkling and eye closure are paralyzed on the affected side due to denervation, whereas in stroke, bilateral cortical innervation spares forehead movement. Over 70-80% of patients recover complete facial motor function spontaneously within 3 to 6 months.",
        "source": "American Academy of Otolaryngology & Mayo Clinic"
    },
    {
        "document_id": "DOC_089",
        "title": "Generalized Anxiety Disorder: DSM-5 Diagnostic Criteria and SSRI First-Line Management",
        "category": "Psychiatry",
        "disease": "Generalized Anxiety Disorder",
        "symptoms": "Excessive, uncontrollable worry occurring on more days than not for >=6 months across various life domains; accompanied by restlessness, feeling keyed-up or on edge, easy fatigability, concentration impairment, muscle tension, and sleep disturbance.",
        "causes": "Complex interplay of neurobiological vulnerabilities (hyperactivity of amygdala-prefrontal circuits, dysregulation of serotonin, norepinephrine, and GABA systems), chronic psychosocial stressors, and genetic heritability.",
        "treatment": "First-line evidence-based pharmacotherapy: Selective Serotonin Reuptake Inhibitors (SSRIs: escitalopram, sertraline) or Serotonin-Norepinephrine Reuptake Inhibitors (SNRIs: venlafaxine, duloxetine); Cognitive Behavioral Therapy (CBT); short-term benzodiazepines strictly reserved for crisis management.",
        "prevention": "Stress-reduction training (mindfulness-based stress reduction, progressive muscle relaxation), regular physical activity, sleep hygiene, and early cognitive therapeutic interventions during acute life stressors.",
        "content": "Generalized Anxiety Disorder (GAD) is a prevalent and disabling psychiatric condition marked by chronic, pervasive, non-circumscribed anxiety and worry about routine everyday matters. The GAD-7 screening tool helps assess symptom severity. Patients frequently present primarily to primary care clinicians with somatic complaints such as chronic tension headaches, muscle aches, insomnia, or gastrointestinal distress. Combining structured cognitive behavioral therapy with first-line antidepressant pharmacotherapy yields the highest sustained response and remission rates.",
        "source": "National Institute of Mental Health & Mayo Clinic"
    },
    {
        "document_id": "DOC_090",
        "title": "Major Depressive Disorder: Monoamine Neurotransmission, DSM-5 Criteria, and Psychotherapy",
        "category": "Psychiatry",
        "disease": "Depression",
        "symptoms": "Persistent depressed mood, pervasive anhedonia (loss of interest or pleasure in activities) for >=2 weeks; significant weight or appetite changes, insomnia or hypersomnia, psychomotor agitation or retardation, fatigue, feelings of worthlessness, impaired concentration, recurrent suicidal ideation.",
        "causes": "Multifactorial pathogenesis involving monoaminergic neurotransmitter dysregulation, impaired neuroplasticity and hippocampal volume reduction (decreased BDNF), hypothalamic-pituitary-adrenal (HPA) axis hyperreactivity, and adverse life events.",
        "treatment": "First-line pharmacotherapy: SSRIs (fluoxetine, sertraline, escitalopram), SNRIs, bupropion, or mirtazapine; evidence-based psychotherapies (Cognitive Behavioral Therapy, Interpersonal Therapy); neuromodulation (Electroconvulsive Therapy [ECT], repetitive Transcranial Magnetic Stimulation [rTMS]) for treatment-resistant depression.",
        "prevention": "Building psychological resilience through social connectedness, regular physical exercise, mindfulness techniques, and early intervention upon emergence of subclinical depressive symptoms.",
        "content": "Major Depressive Disorder (MDD) is a leading cause of global disability and suicidal mortality. The Patient Health Questionnaire-9 (PHQ-9) is widely utilized for screening, baseline staging, and monitoring treatment response. Adequate pharmacotherapeutic trials require therapeutic dosing sustained for at least 4 to 8 weeks before assessing response. Antidepressant discontinuation must be gradual to prevent withdrawal syndromes, and maintenance therapy for 6 to 12 months post-remission is standard to mitigate relapse vulnerability.",
        "source": "American Psychiatric Association & NIMH"
    },

    # 18. ADDITIONAL INFECTIOUS DISEASES & PARASITOLOGY
    {
        "document_id": "DOC_091",
        "title": "Typhoid Fever: Salmonella Typhi Bacteremia, Widal Reaction, and Fluoroquinolone Resistance",
        "category": "Infectious Diseases",
        "disease": "Typhoid Fever",
        "symptoms": "Step-ladder rising sustained high fever, profound headache, relative bradycardia (Faget sign), abdominal pain, hepatosplenomegaly, 'rose spots' (transient erythematous macules on trunk), coated tongue, pea-soup diarrhea or constipation.",
        "causes": "Systemic bacterial infection by Salmonella enterica serotype Typhi (and Paratyphi A, B, C), transmitted via the fecal-oral route through water or food contaminated by chronic carrier feces.",
        "treatment": "Antimicrobial therapy based on susceptibility: azithromycin or third-generation cephalosporins (ceftriaxone) for multidrug-resistant or fluoroquinolone-resistant strains; carbapenems for extensively drug-resistant (XDR) strains; supportive fluid management.",
        "prevention": "Typhoid conjugate vaccines (TCV: Typbar-TCV) providing long-lasting immunity; safe drinking water, sanitary waste disposal, thorough handwashing, and rigorous food hygiene.",
        "content": "Typhoid (enteric) fever is an invasive bacterial infection endemic in regions with deficient water and sanitation infrastructure. Ingested bacilli invade the intestinal mucosa via M cells of Peyer's patches, where they survive intracellularly within mononuclear phagocytes and disseminate into the bloodstream and reticuloendothelial system. Without targeted antibiotic therapy, severe complications arise in the 3rd and 4th weeks: intestinal perforation of ulcerated Peyer's patches and massive gastrointestinal hemorrhage. Blood culture remains the diagnostic gold standard, outperforming unreliable Widal serology.",
        "source": "WHO Guidelines & CDC"
    },
    {
        "document_id": "DOC_092",
        "title": "Cholera: Vibrio cholerae Enterotoxin, Rice-Water Diarrhea, and Oral Rehydration Therapy",
        "category": "Infectious Diseases",
        "disease": "Cholera",
        "symptoms": "Painless, sudden, voluminous profuse watery diarrhea resembling 'rice water', recurrent projectile vomiting, severe muscle cramps in legs, rapid onset of profound hypovolemic dehydration (sunken eyes, loss of skin turgor, cold clammy extremities, anuria).",
        "causes": "Ingestion of food or water contaminated with toxigenic strains of the gram-negative bacterium Vibrio cholerae belonging to serogroups O1 and O139.",
        "treatment": "Aggressive, immediate rehydration: Oral Rehydration Salts (ORS) for mild-to-moderate dehydration; rapid intravenous crystalloids (Ringer's lactate) for severe shock; oral antibiotics (doxycycline, azithromycin) to reduce diarrhea volume and duration; supplemental zinc in children.",
        "prevention": "Provision of safe drinking water and adequate sanitation; oral cholera vaccines (Dukoral, Shanchol, Euvichol) for population protection during outbreaks and complex humanitarian emergencies.",
        "content": "Cholera is an acute, potentially lethal diarrheal disease capable of killing an adult within hours if untreated. The secreted cholera enterotoxin binds to GM1 ganglioside receptors on intestinal enterocytes, activating adenylate cyclase and leading to marked elevation of intracellular cyclic AMP. This activates the CFTR chloride channel, driving massive secretion of chloride, bicarbonate, and water into the intestinal lumen that overwhelms colonic absorptive capacity. Case fatality rates can exceed 50% without rehydration, but plummet to <1% with standard ORS protocols.",
        "source": "WHO Guidelines & CDC"
    },
    {
        "document_id": "DOC_093",
        "title": "Rabies: Lyssavirus Encephalomyelitis, Hydrophobia, and Post-Exposure Prophylaxis",
        "category": "Infectious Diseases",
        "disease": "Rabies",
        "symptoms": "Prodromal pain or tingling at bite site; encephalitic 'furious' rabies: hydrophobia (terror and pharyngeal spasms when attempting to drink), aerophobia, agitation, hallucinations, autonomic hyperactivity; paralytic 'dumb' rabies: ascending paralysis.",
        "causes": "Rabies virus, a neurotropic negative-sense single-stranded RNA rhabdovirus transmitted through saliva via bites, scratches, or mucous membrane contamination from infected mammals (dogs, bats, raccoons, skunks).",
        "treatment": "Once clinical neurological symptoms appear, rabies is virtually 100% fatal; palliative comfort care; experimental Milwaukee protocol has failed to demonstrate reproducible survival.",
        "prevention": "Post-Exposure Prophylaxis (PEP) administered immediately following exposure: thorough wound washing with soap and water for 15 minutes, administration of Rabies Immune Globulin (RIG) infiltrated into the wound, and a 4-dose rabies vaccination series; mass canine vaccination.",
        "content": "Rabies is an acute, progressive, fatal viral encephalomyelitis. Inoculated virus binds to nicotinic acetylcholine receptors at neuromuscular junctions and undergoes retrograde axoplasmic transport along peripheral nerves to the central nervous system. Following replication within spinal cord neurons and brain, centrifugal spread along autonomic nerves delivers high viral titers to salivary glands. Prompt initiation of post-exposure prophylaxis prior to viral invasion of peripheral nerves provides 100% protection against disease development.",
        "source": "WHO Guidelines & CDC"
    },
    {
        "document_id": "DOC_094",
        "title": "Tetanus: Clostridium tetani Tetanolysin, Spasticity, and Trismus (Lockjaw)",
        "category": "Infectious Diseases",
        "disease": "Tetanus",
        "symptoms": "Trismus (painful spasm of masseter muscles / lockjaw), risus sardonicus (characteristic sneering facial spasm), painful generalized muscle spasms, opisthotonos (arching of back and neck), autonomic instability (labile hypertension, tachycardia, hyperpyrexia).",
        "causes": "Contamination of puncture wounds, burns, or devitalized tissue with spores of the obligate anaerobic bacterium Clostridium tetani, which germinate and produce the zinc-metalloprotease neurotoxin tetanospasmin.",
        "treatment": "Wound debridement to remove anaerobic nidus; human tetanus immune globulin (HTIG) to neutralize unbound toxin; intravenous metronidazole or penicillin; muscle spasm control with high-dose benzodiazepines (diazepam) or neuromuscular blockade; mechanical ventilation.",
        "prevention": "Primary childhood immunization with tetanus toxoid-containing vaccines (DTaP/Tdap) with routine booster doses every 10 years throughout adulthood, plus wound management prophylaxis following injury.",
        "content": "Tetanus is a non-communicable neurological disease caused by tetanospasmin neurotoxin. The toxin undergoes retrograde axonal transport to inhibitory interneurons in the spinal cord and brainstem, where it cleaves synaptobrevin (VAMP). This cleaving selectively abolishes the exocytotic release of inhibitory neurotransmitters GABA and glycine from Renshaw cells, producing uncontrolled disinhibition of lower motor neurons and sustained agonist-antagonist muscular spasticity. Mortality occurs from laryngospasm, autonomic storm, or respiratory failure.",
        "source": "CDC & WHO Guidelines"
    },
    {
        "document_id": "DOC_095",
        "title": "Lyme Disease: Borrelia burgdorferi Spirochetes, Erythema Migrans, and Doxycycline",
        "category": "Infectious Diseases",
        "disease": "Lyme Disease",
        "symptoms": "Early localized: expanding annular erythematous rash with central clearing ('bull's-eye' erythema migrans), fatigue, fever, myalgia, arthralgia. Early disseminated: multiple secondary lesions, cranial neuropathy (bilateral Bell's palsy), carditis with AV block. Late: persistent Lyme arthritis.",
        "causes": "Infection with the spirochetal bacterium Borrelia burgdorferi, transmitted via the bite of infected blacklegged ticks (Ixodes scapularis and Ixodes pacificus) attached for >=36-48 hours.",
        "treatment": "Early localized and disseminated disease: oral doxycycline (100 mg twice daily for 10-14 days), amoxicillin, or cefuroxime axetil; intravenous ceftriaxone for advanced neurological manifestations (meningitis) or high-grade cardiac conduction block.",
        "prevention": "Avoiding tick-infested brush habitats, wearing light-colored protective clothing, applying EPA-registered insect repellents (DEET, picaridin) to skin and permethrin to garments, performing prompt whole-body tick checks, and removing ticks with fine-tipped tweezers.",
        "content": "Lyme disease is the most prevalent vector-borne illness in North America and Europe. Clinical diagnosis is established clinically upon detection of an erythema migrans rash in an endemic region without laboratory testing. For extracutaneous manifestations, CDC endorses a two-tier serological testing protocol: initial sensitive enzyme immunoassay (EIA), followed if positive or equivocal by a confirmatory Western blot or second enzyme immunoassay. Post-treatment Lyme Disease Syndrome describes persistent subjective symptoms following complete antibiotic eradication.",
        "source": "CDC & Infectious Diseases Society of America"
    },

    # 19. REPRODUCTIVE, UROLOGY, & ADDITIONAL TOPICS
    {
        "document_id": "DOC_096",
        "title": "Benign Prostatic Hyperplasia: Lower Urinary Tract Symptoms, Alpha-1 Blockers, and 5-ARIs",
        "category": "Urology",
        "disease": "Benign Prostatic Hyperplasia",
        "symptoms": "Lower urinary tract symptoms (LUTS): storage symptoms (urinary frequency, nocturia, urgency) and voiding symptoms (weak urinary stream, hesitancy, intermittency, straining, incomplete bladder emptying).",
        "causes": "Non-malignant proliferation of stromal and epithelial cells within the prostatic transition zone, driven by dihydrotestosterone (DHT) interacting with androgen receptors in aging men.",
        "treatment": "Alpha-1 adrenergic receptor antagonists (tamsulosin, alfuzosin) to relax prostatic smooth muscle; 5-alpha reductase inhibitors (finasteride, dutasteride) to shrink prostatic volume; PDE-5 inhibitors (tadalafil); surgical intervention via transurethral resection of the prostate (TURP) or laser enucleation.",
        "prevention": "Maintaining a healthy body weight, regular physical exercise, moderating caffeine and evening fluid consumption, avoiding over-the-counter decongestants and anticholinergics that provoke urinary retention.",
        "content": "Benign Prostatic Hyperplasia (BPH) is an extremely common age-dependent urological condition, histologically evident in >80% of men older than 70 years. Prostatic enlargement compresses the prostatic urethra, generating mechanical and dynamic bladder outlet obstruction. Evaluation includes the International Prostate Symptom Score (IPSS), digital rectal examination (DRE), urinalysis, serum Prostate-Specific Antigen (PSA), and post-void residual urine volume measurement. Chronic severe obstruction can induce detrusor failure, bilateral hydronephrosis, and postrenal acute kidney injury.",
        "source": "American Urological Association & NIH MedlinePlus"
    },
    {
        "document_id": "DOC_097",
        "title": "Polycystic Ovary Syndrome (PCOS): Rotterdam Criteria, Hyperandrogenism, and Metformin",
        "category": "Endocrinology & Gynecology",
        "disease": "Polycystic Ovary Syndrome",
        "symptoms": "Oligomenorrhea or amenorrhea, clinical or biochemical hyperandrogenism (hirsutism, severe cystic acne, androgenic alopecia), polycystic ovarian morphology on ultrasound, central obesity, acanthosis nigricans, subfertility.",
        "causes": "Complex heterogeneous endocrine disorder characterized by hyperandrogenism, neuroendocrine dysregulation (elevated LH-to-FSH ratio), and peripheral insulin resistance producing compensatory hyperinsulinemia.",
        "treatment": "Lifestyle modification (5-10% weight loss); combined oral contraceptives for menstrual cycle regulation and hyperandrogenism; antiandrogens (spironolactone); insulin sensitizers (metformin); ovulation induction with letrozole or clomiphene citrate for women seeking pregnancy.",
        "prevention": "Adopting healthy dietary practices early in life, routine screening for glucose intolerance (oral glucose tolerance test) and dyslipidemia, and managing weight to mitigate type 2 diabetes and endometrial hyperplasia risks.",
        "content": "Polycystic Ovary Syndrome (PCOS) is the most frequent endocrine disorder among women of reproductive age. The Rotterdam consensus criteria establish diagnosis upon confirming at least two of three features: ovulatory dysfunction, hyperandrogenism, and polycystic ovaries on ultrasound, having excluded mimicking disorders (congenital adrenal hyperplasia, hyperprolactinemia, Cushing syndrome). Chronic anovulation exposes the endometrium to unopposed estrogen, markedly increasing long-term risks of endometrial hyperplasia and carcinoma.",
        "source": "Endocrine Society & American College of Obstetricians and Gynecologists"
    },
    {
        "document_id": "DOC_098",
        "title": "Endometriosis: Ectopic Endometrial Stroma, Pelvic Pain, and Laparoscopic Excision",
        "category": "Gynecology",
        "disease": "Endometriosis",
        "symptoms": "Severe secondary dysmenorrhea (painful menstruation), deep dyspareunia (painful intercourse), chronic non-menstrual pelvic pain, dyschezia (painful defecation during menses), dysuria, subfertility and infertility.",
        "causes": "Presence of functional endometrial glands and stroma outside the uterine cavity (ovaries, uterosacral ligaments, pouch of Douglas). Etiological theories include retrograde menstruation (Sampson's theory), coelomic metaplasia, vascular/lymphatic dissemination, and immune clearance failure.",
        "treatment": "Medical suppression: combined hormonal contraceptives, high-dose progestins, GnRH agonists/antagonists (elagolix, relugolix) with add-back hormone therapy; NSAIDs for pelvic pain; conservative laparoscopic surgical excision of endometriotic implants and adhesiolysis.",
        "prevention": "No established primary prevention; combined hormonal contraceptive use may reduce symptomatic pain and retard progression of lesions.",
        "content": "Endometriosis is an estrogen-dependent chronic inflammatory gynecological disorder affecting approximately 10% of reproductive-aged women globally. Ectopic endometriotic tissue responds cyclicly to ovarian hormones, shedding blood into the peritoneal cavity and precipitating chronic inflammation, fibrosis, and dense pelvic adhesions. Ovarian involvement often forms cystic 'chocolate cysts' (endometriomas). High-resolution transvaginal ultrasound and pelvic MRI assist in detecting deep infiltrating endometriosis, while laparoscopy with histological biopsy serves as the definitive diagnostic standard.",
        "source": "American College of Obstetricians and Gynecologists & WHO Guidelines"
    },
    {
        "document_id": "DOC_099",
        "title": "Glaucoma: Elevated Intraocular Pressure, Optic Nerve Cupping, and Prostaglandin Analogs",
        "category": "Ophthalmology",
        "disease": "Glaucoma",
        "symptoms": "Primary open-angle glaucoma (POAG) is insidious and painless with progressive bilateral peripheral visual field constriction ('tunnel vision'); acute angle-closure glaucoma is an emergency with severe ocular pain, headache, nausea, colored halos around lights, and red steamy cornea.",
        "causes": "Impaired drainage of aqueous humor through the trabecular meshwork leading to elevated intraocular pressure (IOP), mechanical axonal compression, and apoptotic death of retinal ganglion cells.",
        "treatment": "Topical ocular hypotensive drops: prostaglandin analogs (latanoprost, bimatoprost) to increase uveoscleral outflow; beta-blockers (timolol), alpha-2 agonists (brimonidine), carbonic anhydrase inhibitors; selective laser trabeculoplasty (SLT); surgical trabeculectomy or minimally invasive glaucoma surgery (MIGS).",
        "prevention": "Comprehensive routine eye examinations with tonometry, pachymetry, and optic nerve imaging every 1-2 years, particularly for adults aged >=40 years, those with high myopia, or positive family history.",
        "content": "Glaucoma is a group of progressive optic neuropathies characterized by morphological changes at the optic nerve head (optic cup-to-disc ratio excavation or 'cupping') and corresponding visual field deficits. Primary open-angle glaucoma is the leading cause of irreversible blindness globally. In acute angle-closure glaucoma, pupillary block or peripheral iris bowing abruptly seals the iridocorneal angle, precipitating skyrocketing IOP (>50 mmHg) requiring emergent medical IOP-lowering and laser peripheral iridotomy.",
        "source": "American Academy of Ophthalmology & NIH National Eye Institute"
    },
    {
        "document_id": "DOC_100",
        "title": "Cataracts: Crystalline Lens Opacification, Phacoemulsification, and Intraocular Lenses",
        "category": "Ophthalmology",
        "disease": "Cataracts",
        "symptoms": "Gradual, painless, progressive blurriness of vision, dulling or yellowing of color perception, glare and halos around headlights during night driving, poor night vision, frequent changes in eyeglass prescriptions ('second sight').",
        "causes": "Aggregation and oxidation of crystalline lens structural proteins (crystallins) secondary to aging, ultraviolet radiation exposure, smoking, diabetes mellitus, systemic corticosteroid therapy, or ocular trauma.",
        "treatment": "Definitive curative management is ambulatory surgical extraction via modern phacoemulsification (ultrasonic fragmentation of the opaque lens) followed by implantation of a biocompatible synthetic intraocular lens (monofocal, multifocal, or toric IOL).",
        "prevention": "Wearing sunglasses blocking 100% of UVA and UVB radiation, smoking cessation, maintaining tight glycemic control in diabetics, consuming antioxidant-rich diets, and avoiding unnecessary prolonged systemic or topical ophthalmic steroids.",
        "content": "Cataract is defined as any opacification of the normally transparent crystalline lens of the human eye, serving as the foremost cause of remediable blindness worldwide. Morphological subtypes include nuclear sclerotic cataracts (affecting the central lens nucleus), cortical cataracts (wedge-shaped spoke opacities in the lens cortex), and posterior subcapsular cataracts (plaque-like opacity beneath the posterior lens capsule, frequently secondary to steroids or diabetes). Slit-lamp biomicroscopy readily establishes diagnosis and surgical staging.",
        "source": "American Academy of Ophthalmology & WHO"
    },
    {
        "document_id": "DOC_101",
        "title": "Systemic Lupus Erythematosus: Antinuclear Antibodies, Immune Complex Vasculitis, and Hydroxychloroquine",
        "category": "Allergy & Immunology",
        "disease": "Lupus",
        "symptoms": "Malar 'butterfly' rash sparing nasolabial folds, photosensitivity, discoid skin lesions, non-erosive polyarthritis, oral ulcers, serositis (pleurisy, pericarditis), lupus nephritis (proteinuria, cellular casts), autoimmune hemolytic anemia, thrombocytopenia.",
        "causes": "Systemic autoimmune disease driven by defective clearance of apoptotic material, generation of autoantibodies against nuclear antigens (ANA, anti-dsDNA, anti-Smith), and systemic immune-complex deposition in microvasculature.",
        "treatment": "Universal baseline therapy with hydroxychloroquine for all patients to prevent flares and organ damage; systemic corticosteroids for acute exacerbations; immunosuppressants (mycophenolate mofetil, cyclophosphamide, azathioprine); targeted B-cell biologics (belimumab, anifrolumab).",
        "prevention": "Strict photoprotection (broad-spectrum sunscreen, protective clothing) to prevent UV-induced apoptosis and disease flares, smoking cessation, and adherence to maintenance hydroxychloroquine.",
        "content": "Systemic Lupus Erythematosus (SLE) is a prototypical multi-system autoimmune disorder predominantly affecting women of childbearing age. Immune complex deposition activates the classical complement pathway, resulting in hypocomplementemia (low C3 and C4) and widespread inflammatory tissue injury. Lupus nephritis is a major determinant of overall morbidity and mortality, requiring surveillance with routine urinalysis, protein-to-creatinine ratio, and renal biopsy. Antiphospholipid syndrome co-occurs in ~30% of patients, heightening vascular thrombosis and pregnancy loss risks.",
        "source": "American College of Rheumatology & NIH MedlinePlus"
    },
    {
        "document_id": "DOC_102",
        "title": "Anorexia Nervosa and Bulimia Nervosa: Eating Disorders, Medical Complications, and Refeeding Syndrome",
        "category": "Psychiatry & Nutritional",
        "disease": "Eating Disorders",
        "symptoms": "Severe restriction of energy intake leading to significantly low body weight, intense fear of gaining weight, distorted body image (anorexia); recurrent episodes of binge eating followed by compensatory purging behaviors (bulimia); Russell sign (calluses on knuckles), parotid gland hypertrophy, enamel erosion.",
        "causes": "Complex multifactorial etiologies involving neurobiological alterations in serotonin and dopamine reward pathways, genetic vulnerabilities, perfectionistic personality traits, and sociocultural pressures valorizing thinness.",
        "treatment": "Multidisciplinary treatment: medical stabilization, structured nutritional rehabilitation; psychotherapies: Family-Based Treatment (Maudsley approach) for adolescents, Enhanced Cognitive Behavioral Therapy (CBT-E); pharmacotherapy (fluoxetine in bulimia nervosa; olanzapine adjunct in refractory anorexia).",
        "prevention": "Promoting body-positive environments, discouraging extreme dieting and weight teasing in schools and athletic programs, and early identification of abnormal eating patterns.",
        "content": "Eating disorders are severe psychiatric illnesses carrying profound medical complications. Severe malnutrition in anorexia nervosa causes sinus bradycardia, orthostatic hypotension, amenorrhea, leukopenia, and osteoporosis. Rapid reintroduction of carbohydrates in severely malnourished patients triggers refeeding syndrome—characterized by fatal hypophosphatemia, hypokalemia, hypomagnesemia, and cardiac arrhythmias resulting from sudden insulin-mediated intracellular ion shifting. Close electrolyte monitoring is mandatory during early refeeding.",
        "source": "American Psychiatric Association & National Eating Disorders Association"
    },
    {
        "document_id": "DOC_103",
        "title": "Measles (Rubeola): Paramyxovirus Transmission, Koplik Spots, and MMR Vaccination",
        "category": "Infectious Diseases",
        "disease": "Measles",
        "symptoms": "High fever, the classic '3 Cs' (cough, coryza, and conjunctivitis), Koplik spots (small bluish-white spots on an erythematous base on the buccal mucosa), followed by an erythematous maculopapular rash spreading cephalocaudally from hairline to trunk and extremities.",
        "causes": "Measles virus, an enveloped, negative-sense, single-stranded RNA virus belonging to the genus Morbillivirus (family Paramyxoviridae), transmitted via aerosolized respiratory droplets with extreme contagiousness (R0 of 12-18).",
        "treatment": "Supportive management: antipyretics, hydration; high-dose oral Vitamin A supplementation administered on two consecutive days to reduce blindness and pneumonia mortality; airborne infection isolation precautions.",
        "prevention": "Two doses of the live attenuated Measles, Mumps, and Rubella (MMR) vaccine (first dose at 12-15 months, second dose at 4-6 years), conferring over 97% lifelong immunity and establishing robust herd protection when population coverage exceeds 95%.",
        "content": "Measles is one of the most contagious human pathogens known. Following viral replication within the respiratory epithelium and draining lymph nodes, widespread viremia causes profound temporary immune suppression ('immune amnesia') that leaves patients highly susceptible to secondary bacterial infections for months. Major complications include severe pneumonia (the leading cause of measles death in children), acute encephalitis, corneal ulceration, and a fatal late neurodegenerative sequela occurring years later termed subacute sclerosing panencephalitis (SSPE).",
        "source": "WHO Guidelines & CDC"
    },
    {
        "document_id": "DOC_104",
        "title": "Biliary Colic and Acute Cholecystitis: Gallstone Obstruction, Murphy's Sign, and Cholecystectomy",
        "category": "Gastroenterology",
        "disease": "Cholecystitis",
        "symptoms": "Severe constant right upper quadrant (RUQ) or epigastric pain radiating to the right shoulder or back, lasting >4-6 hours, accompanied by fever, leukocytosis, nausea, vomiting, and positive Murphy sign (inspiratory arrest on palpation of RUQ).",
        "causes": "Sustained cystic duct obstruction by an impacted gallstone (calculous cholecystitis in ~95% of cases), causing mechanical gallbladder distention, mucosal ischemia, chemical irritation by lysolecithin, and secondary bacterial infection.",
        "treatment": "Inpatient admission, bowel rest (NPO), intravenous fluid resuscitation, multimodal parenteral analgesia, empiric intravenous broad-spectrum antibiotics (ceftriaxone plus metronidazole); early laparoscopic cholecystectomy within 24-72 hours of admission.",
        "prevention": "Maintaining a healthy body weight, avoiding rapid extreme weight loss which promotes gallstone formation, consuming a diet high in fiber and healthy unsaturated fats, and regular physical activity.",
        "content": "Acute cholecystitis is an inflammatory infection of the gallbladder wall predominantly arising as a complication of cholelithiasis. In contrast to transient biliary colic, the pain of acute cholecystitis persists for more than 6 hours and is accompanied by systemic inflammatory markers. Abdominal ultrasound is the primary initial imaging procedure of choice, revealing gallstones, gallbladder wall thickening (>4 mm), pericholecystic fluid, and a sonographic Murphy sign. Untreated cases risk gangrenous necrosis, gallbladder perforation, and peritonitis.",
        "source": "Tokyo Guidelines & American College of Gastroenterology"
    },
    {
        "document_id": "DOC_105",
        "title": "Sepsis and Septic Shock: Dysregulated Host Response, qSOFA Criteria, and Surviving Sepsis Campaign",
        "category": "Infectious Diseases",
        "disease": "Sepsis",
        "symptoms": "Hypothermia (<36°C) or hyperthermia (>38.3°C), severe tachycardia (>90 bpm), tachypnea (>20 bpm), acute confusion or encephalopathy, extreme shivering or muscle pain, mottled cold skin, oliguria, hypotension unresponsive to initial fluid resuscitation.",
        "causes": "Life-threatening organ dysfunction caused by a dysregulated systemic host response to an infection (pneumonia, UTI, intra-abdominal sepsis, skin/soft tissue infection), triggering widespread endothelial injury, capillary leak, and microvascular thrombosis.",
        "treatment": "The 'Surviving Sepsis Hour-1 Bundle': measure blood lactate level; obtain blood cultures prior to antibiotics; administer empiric broad-spectrum intravenous antimicrobials; rapid infusion of 30 mL/kg crystalloids for hypotension or lactate >=4 mmol/L; administer vasopressors (norepinephrine first-line) to maintain mean arterial pressure (MAP) >=65 mmHg.",
        "prevention": "Preventing infections through vaccination (influenza, pneumococcus), sterile surgical and catheter techniques in hospitals, prompt treatment of localized infections (UTIs, cellulitis, pneumonia), and good community hygiene.",
        "content": "Sepsis is a major global healthcare crisis accounting for approximately 20% of all global deaths. The Sepsis-3 consensus definition defines sepsis as an acute change in total Sequential Organ Failure Assessment (SOFA) score >=2 points consequent to infection. Septic shock represents a subset where underlying circulatory and cellular/metabolic abnormalities are profound enough to substantially increase mortality, identified by persistent hypotension requiring vasopressors to maintain MAP >=65 mmHg and serum lactate >2 mmol/L despite adequate fluid resuscitation.",
        "source": "Surviving Sepsis Campaign Guidelines & WHO"
    }
]

EVALUATION_QUERIES = [
    {
        "query_id": "Q001",
        "query": "What are common symptoms of diabetes?",
        "relevant_document_ids": "DOC_001,DOC_002,DOC_003"
    },
    {
        "query_id": "Q002",
        "query": "What causes high blood pressure and essential hypertension?",
        "relevant_document_ids": "DOC_006,DOC_007,DOC_008"
    },
    {
        "query_id": "Q003",
        "query": "What are common asthma triggers and symptoms?",
        "relevant_document_ids": "DOC_011,DOC_012"
    },
    {
        "query_id": "Q004",
        "query": "How is dengue transmitted and how can it be prevented?",
        "relevant_document_ids": "DOC_018,DOC_019"
    },
    {
        "query_id": "Q005",
        "query": "What are the symptoms and causes of iron deficiency anemia?",
        "relevant_document_ids": "DOC_031"
    },
    {
        "query_id": "Q006",
        "query": "What causes migraine headaches and what medications are used for treatment?",
        "relevant_document_ids": "DOC_026,DOC_027"
    },
    {
        "query_id": "Q007",
        "query": "What are the symptoms of community-acquired pneumonia?",
        "relevant_document_ids": "DOC_013,DOC_014"
    },
    {
        "query_id": "Q008",
        "query": "How can food poisoning and bacterial contamination be prevented?",
        "relevant_document_ids": "DOC_044,DOC_045"
    },
    {
        "query_id": "Q009",
        "query": "What is the difference between osteoarthritis and rheumatoid arthritis?",
        "relevant_document_ids": "DOC_036,DOC_037"
    },
    {
        "query_id": "Q010",
        "query": "How is malaria diagnosed and what is the recommended treatment?",
        "relevant_document_ids": "DOC_020,DOC_021"
    },
    {
        "query_id": "Q011",
        "query": "What are the clinical features and transmission of pulmonary tuberculosis?",
        "relevant_document_ids": "DOC_022,DOC_023"
    },
    {
        "query_id": "Q012",
        "query": "What causes acute kidney injury and how does it differ from chronic kidney disease?",
        "relevant_document_ids": "DOC_046,DOC_047"
    },
    {
        "query_id": "Q013",
        "query": "What are the warning signs and phases of severe dengue fever?",
        "relevant_document_ids": "DOC_018,DOC_019"
    },
    {
        "query_id": "Q014",
        "query": "How does vitamin B12 deficiency cause anemia and neurological problems?",
        "relevant_document_ids": "DOC_032"
    },
    {
        "query_id": "Q015",
        "query": "What is diabetic ketoacidosis and how is it managed in emergency care?",
        "relevant_document_ids": "DOC_004,DOC_002"
    },
    {
        "query_id": "Q016",
        "query": "What are the common symptoms and treatment of acute gastritis and peptic ulcers?",
        "relevant_document_ids": "DOC_041,DOC_042"
    },
    {
        "query_id": "Q017",
        "query": "What causes non-alcoholic fatty liver disease and liver cirrhosis?",
        "relevant_document_ids": "DOC_051,DOC_052"
    },
    {
        "query_id": "Q018",
        "query": "What are the symptoms and emergency treatment for acute anaphylaxis?",
        "relevant_document_ids": "DOC_057,DOC_060"
    },
    {
        "query_id": "Q019",
        "query": "How does chronic obstructive pulmonary disease develop and how is it managed?",
        "relevant_document_ids": "DOC_015"
    },
    {
        "query_id": "Q020",
        "query": "What is the role of vitamin D in bone health and rickets prevention?",
        "relevant_document_ids": "DOC_034,DOC_040"
    },
    {
        "query_id": "Q021",
        "query": "What are the signs of congestive heart failure and fluid overload?",
        "relevant_document_ids": "DOC_010,DOC_009"
    },
    {
        "query_id": "Q022",
        "query": "What causes gout and how is hyperuricemia treated?",
        "relevant_document_ids": "DOC_038"
    },
    {
        "query_id": "Q023",
        "query": "What are the long-term complications and symptoms of Long COVID?",
        "relevant_document_ids": "DOC_025,DOC_024"
    },
    {
        "query_id": "Q024",
        "query": "What are the symptoms and causes of kidney stones?",
        "relevant_document_ids": "DOC_048"
    },
    {
        "query_id": "Q025",
        "query": "How is hepatitis B transmitted and prevented by vaccination?",
        "relevant_document_ids": "DOC_053,DOC_054"
    },
    {
        "query_id": "Q026",
        "query": "What are the classic symptoms of Parkinson's disease?",
        "relevant_document_ids": "DOC_028"
    },
    {
        "query_id": "Q027",
        "query": "How is ischemic stroke identified using the FAST criteria?",
        "relevant_document_ids": "DOC_029"
    },
    {
        "query_id": "Q028",
        "query": "What is Hashimoto's thyroiditis and how is hypothyroidism treated?",
        "relevant_document_ids": "DOC_061"
    },
    {
        "query_id": "Q029",
        "query": "What are the diagnostic criteria for metabolic syndrome and obesity?",
        "relevant_document_ids": "DOC_063,DOC_064"
    },
    {
        "query_id": "Q030",
        "query": "What causes celiac disease and why must gluten be avoided?",
        "relevant_document_ids": "DOC_066"
    },
    {
        "query_id": "Q031",
        "query": "What is the difference between Crohn's disease and ulcerative colitis?",
        "relevant_document_ids": "DOC_067,DOC_068"
    },
    {
        "query_id": "Q032",
        "query": "What are the symptoms and emergency signs of bacterial meningitis?",
        "relevant_document_ids": "DOC_074"
    },
    {
        "query_id": "Q033",
        "query": "How is pulmonary embolism diagnosed and treated with anticoagulants?",
        "relevant_document_ids": "DOC_076,DOC_085"
    },
    {
        "query_id": "Q034",
        "query": "What is atrial fibrillation and how does it increase stroke risk?",
        "relevant_document_ids": "DOC_081,DOC_029"
    },
    {
        "query_id": "Q035",
        "query": "What are the symptoms and prevention protocol for sepsis and septic shock?",
        "relevant_document_ids": "DOC_105"
    }
]

def generate():
    os.makedirs("data", exist_ok=True)
    doc_path = os.path.join("data", "medical_documents.csv")
    fieldnames = [
        "document_id", "title", "category", "disease", "symptoms",
        "causes", "treatment", "prevention", "content", "source"
    ]
    with open(doc_path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for doc in DOCUMENTS:
            writer.writerow(doc)
    print(f"Successfully generated {len(DOCUMENTS)} medical documents in {doc_path}")

    eval_path = os.path.join("data", "evaluation_queries.csv")
    eval_fieldnames = ["query_id", "query", "relevant_document_ids"]
    with open(eval_path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=eval_fieldnames)
        writer.writeheader()
        for q in EVALUATION_QUERIES:
            writer.writerow(q)
    print(f"Successfully generated {len(EVALUATION_QUERIES)} evaluation queries in {eval_path}")

if __name__ == "__main__":
    generate()
