# Taxonomy Selection for Medical Imaging AI Reviews

Use this file only for narrative reviews and method surveys. For scoping and systematic reviews, let the protocol determine the Results structure; use taxonomy labels only inside extraction tables or synthesis text.

The entries below are organizational prompts, not a source of factual claims. Verify every named method, dataset, product, and performance statement through the normal evidence workflow before using it in a manuscript.

## Choose the organizing logic

Select the structure that best answers the review question. Record the choice and rejected alternatives in `<project_dir>/REVIEW_CONTEXT.md`.

| Review question | Preferred structure |
|---|---|
| How do model-design choices differ? | Architecture / inductive prior / data regime |
| How does a pipeline solve a clinical task? | Acquisition / localization / segmentation or classification / quantification / decision support |
| How mature is the evidence? | Development / internal validation / external validation / reader study / implementation |
| Where does AI enter clinical care? | Referral / acquisition / interpretation / reporting / intervention / monitoring |
| What prevents deployment? | Data / model / human factors / workflow / regulation / monitoring |

Do not force a three-axis method taxonomy onto a diagnostic-accuracy, implementation, economic, regulatory, or evidence-maturity review.

## Method-design structure

When the question is method-heavy, three complementary axes are often useful:

1. **Architecture** — how information is represented and propagated, such as convolutional, transformer, state-space, graph, temporal, or hybrid designs.
2. **Inductive prior** — what task-specific constraint is encoded, such as anatomy, topology, boundary, shape, uncertainty, multi-task, or physics constraints.
3. **Data regime** — how supervision and data access are organized, such as self-supervised, weakly supervised, semi-supervised, foundation-model adaptation, domain adaptation, federated, or continual learning.

Treat these as comparison dimensions, not mutually exclusive bins. Assign each study a primary axis for exposition and record secondary axes in the synthesis matrix.

## Domain prompts

Use only the prompts relevant to the question. They are intentionally non-exhaustive.

### Cardiovascular CT and MR

- Vessel, chamber, myocardium, plaque, flow, and tissue characterization tasks
- Centerline, topology, shape, temporal, and multi-modality priors
- Segmentation, quantification, prognosis, and decision-support stages
- Site, scanner, protocol, and patient-population transportability

### Lung CT and chest radiography

- Detection, segmentation, classification, triage, and longitudinal assessment
- Two-dimensional versus three-dimensional context
- Multi-scale, boundary, uncertainty, and report-supervision strategies
- Screening prevalence, threshold selection, and external-site validation

### Brain CT and MRI

- Multi-sequence fusion, registration, segmentation, detection, and prognosis
- Spatial, temporal, atlas, connectivity, and longitudinal priors
- Missing-sequence robustness and acquisition heterogeneity
- External validation across sites, scanners, and populations

### Echocardiography and non-coronary ultrasound

(Cardiac CT/MR live in "Cardiovascular CT and MR" above; this section covers
ultrasound-first cardiac work — echo, Doppler, point-of-care ultrasound.)

- Cine, multi-view, Doppler, deformation, and temporal modeling
- Operator and acquisition dependence
- Shape, motion, anatomy, and uncertainty constraints
- Reader interaction, workflow timing, and repeatability

### Digital pathology

- Patch, slide, region, cell, and graph representations
- Multiple-instance, weakly supervised, self-supervised, and foundation-model regimes
- Pre-analytic variation, scanner shift, stain variation, and site generalization
- Biomarker, grading, prognosis, and clinical workflow endpoints

### Retinal and ophthalmic imaging

- Fundus, OCT, angiography, segmentation, grading, and progression tasks
- Device shift, image quality, domain adaptation, and longitudinal modeling
- Screening thresholds, subgroup performance, and referral consequences

### Breast imaging and mammography

- Mammography (2D/tomosynthesis), ultrasound, and MRI screening tasks
- Prevalence, recall, and threshold effects on measured performance
- Regulatory density: CADe/CADx pathways, locked-model claims, and post-market surveillance evidence
- Dense-breast protocols, supplemental screening, and interval-cancer analysis

### Abdominal and oncologic imaging

- Liver (CT/MR including LI-RADS), prostate mpMRI, pancreatic, and kidney tasks
- Lesion detection/characterization, response assessment (RECIST and beyond), and multi-phase priors
- Multi-parametric fusion, organ-specific atlases, and longitudinal change modeling
- Screening-trial evidence and multi-site oncologic workflow endpoints

### Musculoskeletal imaging

- Radiographs, CT, and MRI of joints, spine, and trauma tasks
- Fracture detection/grading, cartilage and ligament assessment, degenerative staging
- Anatomic priors, bilateral symmetry, and view-standardization strategies
- Emergency workflow integration, triage prioritization, and reader-substitution evidence

### Nuclear medicine and molecular imaging

- PET/CT, PET/MR, SPECT: uptake quantification (SUV), lesion detection, and treatment-response tasks
- PSMA/FDG and theranostic applications; tracer-specific priors
- Attenuation/segmentation coupling, motion, and partial-volume effects
- Quantitative reproducibility, phantom standardization, and multicenter calibration

### Acquisition-side AI: reconstruction, denoising, and acceleration

(For method surveys this is often a primary axis rather than a downstream task.)

- Compressed sensing / deep-learning reconstruction, denoising, super-resolution, and acquisition acceleration
- Artifact suppression (motion, metal, undersampling) and its downstream diagnostic effect
- Reconstruction-objective vs diagnostic-task trade-offs; loss-function design
- Scanner-vendor generalization, dose/scan-time claims, and blinded-reader validation

### Cross-modality or general segmentation

- Architecture, task prior, and data regime as the initial comparison frame
- Modality-specific acquisition and annotation differences as explicit modifiers
- Dataset split integrity, benchmark comparability, and external validation as separate evidence dimensions

## Fit check before drafting

Confirm all of the following:

- The taxonomy answers the stated review question rather than merely classifying papers.
- Important studies do not require repeated or artificial placement.
- Clinical evidence and implementation evidence are not hidden inside an architecture section.
- Categories remain stable when new studies are added.
- The taxonomy supports comparison and synthesis, not a flat catalogue.

If the fit is poor, switch structures before drafting. Do not add more same-depth headings merely to preserve the initial taxonomy.

## Examples

For an illustrative, non-citable cardiovascular taxonomy, see [`../examples/ccta-taxonomy-example.md`](../examples/ccta-taxonomy-example.md). Reverify all named concepts before adapting it.
