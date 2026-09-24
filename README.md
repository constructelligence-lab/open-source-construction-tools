# Open source construction tools

A list of open source software that actually gets used in construction, building and infrastructure work —
and, just as importantly, an honest note on what each one is *not* good for.

Most lists in this space are written by people who have never had to explain a schedule slip. This one is
narrower on purpose: every project here has been checked against the GitHub API for its licence, language,
last commit and archived status, so you can see at a glance whether you are looking at something maintained
or something abandoned in 2019.

## How to read this list

- **Licence and activity are read from the API, not typed by hand.** Both matter more than star counts. A
  permissive licence (MIT, Apache-2.0, BSD) lets you embed the code in something you sell; a copyleft licence
  (GPL, AGPL) usually does not, without obligations you should read properly. AGPL in particular catches
  people who only plan to offer a hosted service.
- **"Last commit" is the abandonment check.** Anything that has not moved in two years is either finished or
  forgotten, and you should find out which before you build on it.
- **Stars measure attention, not fitness.** A popular library with the wrong licence for your product is
  still the wrong library.
- **The caveat column is the point.** Every tool here is good at something narrower than its README suggests.
- **Nothing here is a recommendation for a specific project.** Validate against your own work, your own data
  and your own contracts.

<!-- begin:index -->
*80 projects checked against the GitHub API on 2026-09-24. Licence, language, last commit and archived status are read from the API, not typed by hand.*

### BIM and IFC

Model authoring, IFC parsing and model servers. The strongest open source area in construction.

| Project | What it does in a construction workflow | Caveat | Licence | Language | Last commit |
| --- | --- | --- | --- | --- | --- |
| [IfcOpenShell](https://github.com/IfcOpenShell/IfcOpenShell) | IFC toolkit in C++ and Python, and the home of Bonsai, a Blender-based BIM authoring environment | Scripting knowledge helps a lot; the Blender interface is not a drafting package | LGPL-3.0 | C++ | 2026-09-24 |
| [BIMserver](https://github.com/opensourceBIM/BIMserver) | Self-hosted IFC model server with revision control and notifications | Java, heavyweight, and the operational effort is real | AGPL-3.0 | Java | 2026-03-13 |
| [web-ifc](https://github.com/ThatOpen/engine_web-ifc) | WebAssembly IFC parser for the browser: geometry and properties at full speed | Parsing only; you bring the interface and the workflows | MPL-2.0 | TypeScript | 2026-09-23 |
| [Speckle](https://github.com/specklesystems/speckle-server) | Open data platform that moves geometry and data between AEC tools | Server to run; check the licence for commercial hosting | custom | TypeScript | 2026-09-24 |
| [ThatOpen Components](https://github.com/ThatOpen/engine_components) | Web components for viewing, measuring and coordinating IFC models in a browser | The successor to IFC.js and still moving; pin your versions | MIT | TypeScript | 2026-09-11 |
| [xBim Essentials](https://github.com/xBimTeam/XbimEssentials) | .NET toolkit for reading, writing and querying IFC | The .NET option; smaller community than IfcOpenShell | custom | C# | 2026-08-28 |
| [BIMsurfer](https://github.com/opensourceBIM/BIMsurfer) | Browser-based IFC viewer used by BIMserver | A viewer, not a coordination or clash tool | MIT | JavaScript | 2025-12-30 |
| [xBim Windows UI](https://github.com/xBimTeam/XbimWindowsUI) | Windows desktop IFC viewer, validation and model tools | Desktop .NET heritage; check the release cadence before depending on it | custom | C# | 2026-08-24 |
| [xBim WebUI](https://github.com/xBimTeam/XbimWebUI) | Web-based IFC model viewer from the xBim project | Viewer only; lighter maintenance than the desktop stack | custom | TypeScript | 2025-10-31 |
| [Bldrs Share](https://github.com/bldrs-ai/Share) | Browser IFC review and collaboration, with links you can share | Young project; validate against your own models first | AGPL-3.0 | JavaScript | 2026-09-24 |

### CAD and drawing

Drawing production, and the PDF and OCR plumbing most document workflows end up needing.

| Project | What it does in a construction workflow | Caveat | Licence | Language | Last commit |
| --- | --- | --- | --- | --- | --- |
| [Stirling PDF](https://github.com/Stirling-Tools/Stirling-PDF) | Self-hosted PDF toolbox: merge, split, stamp, OCR, redact, compress | General purpose; it knows nothing about sheets and revisions | custom | Java | 2026-09-24 |
| [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR) | OCR with strong layout and table understanding | Model downloads and GPU expectations; keep documents in-house | Apache-2.0 | Python | 2026-09-16 |
| [Tesseract](https://github.com/tesseract-ocr/tesseract) | The OCR engine behind most document digitisation | Accuracy collapses on stamped, folded, hand-annotated drawings | Apache-2.0 | C++ | 2026-09-11 |
| [pdf.js](https://github.com/mozilla/pdf.js) | PDF rendering in the browser; the base layer of most web drawing viewers | Rendering and forms, not measurement or markup workflows | Apache-2.0 | JavaScript | 2026-09-24 |
| [FreeCAD](https://github.com/FreeCAD/FreeCAD) | Parametric 3D CAD with BIM, FEM and drawing workbenches | Real learning curve; a modelling tool rather than a construction platform | LGPL-2.1 | C++ | 2026-09-24 |
| [pdfplumber](https://github.com/jsvine/pdfplumber) | Extracts text, tables and coordinates from PDFs | Text-based PDFs only; scanned sets need OCR first | MIT | Python | 2026-08-06 |
| [PyMuPDF](https://github.com/pymupdf/PyMuPDF) | Fast PDF parsing, text extraction and manipulation in Python | AGPL for the free tier: check before embedding in a product | AGPL-3.0 | Python | 2026-09-24 |
| [LibreCAD](https://github.com/LibreCAD/LibreCAD) | 2D CAD for drawing production | 2D only, and DWG support is weaker than DXF: convert first | custom | C++ | 2026-09-24 |
| [Camelot](https://github.com/atlanhq/camelot) *(archived)* | Pulls tables out of PDFs into dataframes | Merged cells and borderless tables defeat it | custom | Python | 2023-01-05 |
| [QCAD](https://github.com/qcad/qcad) | 2D CAD with a mature DXF/DWG engine | Community edition is GPL; some features are paid editions | custom | C++ | 2026-09-24 |
| [ezdxf](https://github.com/mozman/ezdxf) | Python library to read, write and automate DXF drawings | A library, not a CAD interface; excellent for drawing QA scripts | MIT | Python | 2026-08-26 |

### Documents and records

Document management and archives, one step removed from proper EDMS.

| Project | What it does in a construction workflow | Caveat | Licence | Language | Last commit |
| --- | --- | --- | --- | --- | --- |
| [Paperless-ngx](https://github.com/paperless-ngx/paperless-ngx) | Scans, indexes and archives documents with tags and full-text search | An archive, not an EDMS: no transmittals, revisions or approval workflow | GPL-3.0 | Python | 2026-09-24 |
| [BookStack](https://github.com/BookStackApp/BookStack) | Wiki-style knowledge base for procedures and O&M documentation | Uncontrolled documentation: not a substitute for a document control system | MIT | PHP | 2026-09-24 |
| [Mayan EDMS](https://github.com/mayan-edms/mayan-edms) | Document management with metadata, versioning and workflow | Setup effort is high and the interface shows its age | custom | Python | 2026-05-23 |

### Scheduling and planning

Gantt and CPM tools, plus the optimisation libraries you build a scheduler on.

| Project | What it does in a construction workflow | Caveat | Licence | Language | Last commit |
| --- | --- | --- | --- | --- | --- |
| [OpenProject](https://github.com/opf/openproject) | Project management with Gantt charts, work packages, budgets and costs | Not a CPM engine: no float analysis or claim-grade schedule reporting | GPL-3.0 | Ruby | 2026-09-24 |
| [OR-Tools](https://github.com/google/or-tools) | Google's optimisation toolkit, including CP-SAT for scheduling and sequencing | You supply the model; it is not a scheduling application | Apache-2.0 | C++ | 2026-09-24 |
| [GanttProject](https://github.com/bardsoftware/ganttproject) | Desktop Gantt charting and critical path scheduling | Basic resource handling; not scaled to multi-job construction programmes | GPL-3.0 | Java | 2026-09-23 |
| [TaskJuggler](https://github.com/taskjuggler/TaskJuggler) | Text-based project planning with real resource levelling | Batch and syntax-heavy; you edit a plan file rather than a chart | GPL-2.0 | Ruby | 2025-07-28 |

### Field data collection

Forms, inspections and field records on a phone, without a commercial platform.

| Project | What it does in a construction workflow | Caveat | Licence | Language | Last commit |
| --- | --- | --- | --- | --- | --- |
| [ODK Collect](https://github.com/getodk/collect) | Android client for filling in ODK forms offline and syncing later | Android only; iOS needs a replacement in the field | custom | Kotlin | 2026-09-24 |
| [ODK Central](https://github.com/getodk/central) | Self-hosted server for mobile field forms, submissions and exports | Not construction-aware: you design the forms and the workflow | Apache-2.0 | JavaScript | 2026-09-23 |
| [KoboToolbox](https://github.com/kobotoolbox/kpi) | Form builder and data collection platform with a mature offline story | The hosted service is the easy path; self-hosting is real work | AGPL-3.0 | Python | 2026-09-24 |

### Reality capture and survey

Photogrammetry, point clouds and the libraries that process them.

| Project | What it does in a construction workflow | Caveat | Licence | Language | Last commit |
| --- | --- | --- | --- | --- | --- |
| [Open3D](https://github.com/isl-org/Open3D) | Point cloud, mesh and registration algorithms in Python and C++ | A library, not an application; you build the workflow | custom | C++ | 2026-09-16 |
| [Meshroom](https://github.com/alicevision/Meshroom) | Photogrammetry with a node-based graphical interface | GPU hungry, and photogrammetry is not measurement-grade surveying | custom | Python | 2026-09-24 |
| [COLMAP](https://github.com/colmap/colmap) | Structure-from-motion and multi-view stereo photogrammetry | Research-grade interface; command line heavy | custom | C++ | 2026-09-24 |
| [OpenDroneMap](https://github.com/OpenDroneMap/ODM) | Turns drone imagery into maps, point clouds and 3D models | Needs good overlap and ground control; outputs still need QA against survey | AGPL-3.0 | Python | 2026-09-16 |
| [Potree](https://github.com/potree/potree) | Web viewer for very large point clouds | Display and navigation only | custom | JavaScript | 2026-01-08 |
| [CloudCompare](https://github.com/CloudCompare/CloudCompare) | Inspect, compare, measure and clean point clouds and meshes | Desktop tool with no project database or audit trail | custom | C++ | 2026-09-24 |
| [PDAL](https://github.com/PDAL/PDAL) | Point cloud data abstraction with pipeline processing | Format and pipeline plumbing rather than end user tooling | custom | C++ | 2026-09-24 |
| [laspy](https://github.com/laspy/laspy) | Read and write LAS and LAZ point cloud files in Python | File format plumbing; pair it with something that analyses | custom | Python | 2026-05-30 |

### GIS and site

Site mapping, terrain and coordinate reference systems.

| Project | What it does in a construction workflow | Caveat | Licence | Language | Last commit |
| --- | --- | --- | --- | --- | --- |
| [QGIS](https://github.com/qgis/QGIS) | Desktop GIS used for site mapping, earthwork volumetrics and utility records | Not CAD: plan production and sheet setup are limited | GPL-2.0 | C++ | 2026-09-24 |
| [GDAL](https://github.com/OSGeo/gdal) | The geospatial translation and processing library under almost everything else | Command line and API only; unglamorous and everywhere | custom | C++ | 2026-09-22 |
| [GeoServer](https://github.com/geoserver/geoserver) | Serves map layers over OGC web services to browsers and apps | Java stack with real operational overhead | custom | Java | 2026-09-24 |
| [pyproj](https://github.com/pyproj4/pyproj) | Coordinate reference system transformations in Python | Choosing the wrong CRS is still your problem, silently | MIT | Python | 2026-09-16 |
| [WhiteboxTools](https://github.com/jblindsay/whitebox-tools) | Terrain, hydrology and raster analysis for earthwork and drainage | Terrain analysis focus; not a survey adjustment tool | MIT | Rust | 2026-05-26 |

### Structural and analysis

Section, frame and nonlinear analysis for engineers who script.

| Project | What it does in a construction workflow | Caveat | Licence | Language | Last commit |
| --- | --- | --- | --- | --- | --- |
| [OpenSees](https://github.com/OpenSees/OpenSees) | Nonlinear structural analysis, widely used in earthquake engineering | Research-grade complexity and steeper than a frame tool | custom | C++ | 2026-09-18 |
| [PyNite](https://github.com/JWock82/PyNite) | 3D frame finite element analysis in Python | Frame elements; it is not a design code checker | MIT | Python | 2026-09-24 |
| [sectionproperties](https://github.com/robbievanleeuwen/section-properties) | Cross-section properties, stress and capacity calculations | Sections only, not whole-structure behaviour | MIT | Python | 2026-04-16 |
| [anaStruct](https://github.com/ritchie46/anaStruct) | 2D frame and truss analysis with plotting | Two dimensions only; teaching to practice grade | LGPL-3.0 | Python | 2026-09-18 |
| [COMPAS](https://github.com/compas-dev/compas) | Computational framework for structural geometry, analysis and fabrication | Python, research-flavoured, and its own learning curve | MIT | Python | 2026-09-08 |
| [OpenSeesPy](https://github.com/zhuminjie/OpenSeesPy) | Python interface to OpenSees for scripting analyses | The packaging and docs repository for OpenSeesPy; same complexity as OpenSees | custom | C++ | 2026-08-18 |

### Energy MEP and sustainability

Simulation and assessment engines: energy, daylight, CFD, LCA.

| Project | What it does in a construction workflow | Caveat | Licence | Language | Last commit |
| --- | --- | --- | --- | --- | --- |
| [OpenFOAM](https://github.com/OpenFOAM/OpenFOAM-dev) | CFD for wind, smoke, ventilation and airflow studies | Specialist tooling: meshing, not modelling, is the hard part | custom | C++ | 2026-09-23 |
| [EnergyPlus](https://github.com/NREL/EnergyPlus) | Whole-building energy simulation, the reference engine in the field | Input files are unforgiving; garbage in, garbage out at scale | custom | C++ | 2026-09-24 |
| [CoolProp](https://github.com/CoolProp/CoolProp) | Thermophysical property database for HVAC and refrigeration calculation | A library; the engineering judgement stays with you | MIT | C++ | 2026-09-24 |
| [OpenStudio](https://github.com/NREL/OpenStudio) | SDK and tooling around EnergyPlus for modelling workflows | Version drift between SDK, GUIs and measures is a known pain | custom | C++ | 2026-09-22 |
| [eemeter](https://github.com/openeemeter/eemeter) | Normalises meter data into energy savings figures | Aimed at utility programme evaluation rather than site work | Apache-2.0 | Python | 2026-09-09 |
| [Ladybug](https://github.com/ladybug-tools/ladybug) | Climate, sun, wind and comfort analysis from weather data | Grasshopper-centric in practice | AGPL-3.0 | Python | 2026-09-22 |
| [Radiance](https://github.com/LBNL-ETA/Radiance) | Daylight and lighting simulation | Decades-old interface; script it or use it through Honeybee | none declared | Shell | 2026-08-20 |
| [Honeybee](https://github.com/ladybug-tools/honeybee) | Daylight and energy modelling built on Radiance and EnergyPlus | Needs Grasshopper or Python skill; not a design tool by itself | GPL-3.0 | Python | 2022-12-27 |
| [Brightway](https://github.com/brightway-lca/brightway25) | Python framework for life cycle assessment (Brightway 2.5) | Version churn is real: 2.5 and 2.x are not interchangeable | BSD-3-Clause | Jupyter Notebook | 2025-11-27 |

### Machine learning and datasets

Detection and segmentation tooling, and the datasets that come with it.

| Project | What it does in a construction workflow | Caveat | Licence | Language | Last commit |
| --- | --- | --- | --- | --- | --- |
| [Ultralytics YOLO](https://github.com/ultralytics/ultralytics) | Object detection and segmentation; the usual starting point for PPE and progress detection | You must train on your own site imagery; published models do not transfer for free | AGPL-3.0 | Python | 2026-09-24 |
| [Segment Anything](https://github.com/facebookresearch/segment-anything) | Promptable image segmentation | Check the weights licence for commercial use before building on it | Apache-2.0 | Jupyter Notebook | 2024-09-18 |
| [Detectron2](https://github.com/facebookresearch/detectron2) | Detection and segmentation toolkit from Meta AI | Research maintenance cadence; expect to pin versions | Apache-2.0 | Python | 2026-08-19 |
| [RoadDamageDetector](https://github.com/sekilab/RoadDamageDetector) | Road damage image dataset and detection baselines | One country's roads: treat it as a benchmark, not a trained model for your site | MIT | Jupyter Notebook | 2025-10-23 |

### Cost accounting and ERP

General ERPs you can shape into job costing, and accounting basics.

| Project | What it does in a construction workflow | Caveat | Licence | Language | Last commit |
| --- | --- | --- | --- | --- | --- |
| [Odoo](https://github.com/odoo/odoo) | ERP with project, timesheet and analytic accounting | Community edition has no construction apps; licensing differs between editions | custom | Python | 2026-09-24 |
| [ERPNext](https://github.com/frappe/erpnext) | Open ERP with projects, timesheets, purchasing and accounting | Not construction-native: no AIA billing, WIP schedule or retainage without customisation | GPL-3.0 | Python | 2026-09-24 |
| [Dolibarr](https://github.com/Dolibarr/dolibarr) | ERP and CRM for small organisations, with invoicing and projects | Job costing is thin for construction | GPL-3.0 | PHP | 2026-09-24 |
| [GnuCash](https://github.com/Gnucash/gnucash) | Double-entry accounting for small businesses | No job costing at construction scale; fine for a tiny outfit only | custom | C | 2026-09-24 |
| [Tryton](https://github.com/tryton/tryton) | Modular ERP with accounting, projects and timesheets | You build the construction layer yourself | none declared | Python | 2026-09-23 |

### Collaboration and PM

Project tracking, wikis, files and chat for the office and the site trailer.

| Project | What it does in a construction workflow | Caveat | Licence | Language | Last commit |
| --- | --- | --- | --- | --- | --- |
| [Plane](https://github.com/makeplane/plane) | Issue and project tracking with cycles and modules | Generic project tooling; no construction workflow built in | AGPL-3.0 | TypeScript | 2026-09-24 |
| [Outline](https://github.com/outline/outline) | Team knowledge base for procedures and standards | A wiki; discipline still decides whether it stays current | custom | TypeScript | 2026-09-24 |
| [Mattermost](https://github.com/mattermost/mattermost) | Self-hosted team chat with file sharing and integrations | Ops burden, and the mobile app matters on site | custom | TypeScript | 2026-09-24 |
| [Nextcloud](https://github.com/nextcloud/server) | Self-hosted file sharing, document collaboration and office integration | File sharing, not document control: no transmittals or revisions | AGPL-3.0 | PHP | 2026-09-24 |
| [Zulip](https://github.com/zulip/zulip) | Threaded team chat, which suits project discussions better than channels | Operational effort to host; adoption is the real risk | Apache-2.0 | Python | 2026-09-24 |
| [Vikunja](https://github.com/go-vikunja/vikunja) | Self-hosted task and project lists | Lightweight by design; no scheduling or costing | AGPL-3.0 | Go | 2026-09-24 |

### Automation robotics and fabrication

Shop automation and robot middleware, where the field robotics work starts.

| Project | What it does in a construction workflow | Caveat | Licence | Language | Last commit |
| --- | --- | --- | --- | --- | --- |
| [OctoPrint](https://github.com/OctoPrint/OctoPrint) | Web control for 3D printers | Prototyping and small-scale fabrication | AGPL-3.0 | Python | 2026-09-22 |
| [ROS 2](https://github.com/ros2/ros2) | Robot middleware: perception, navigation and control architecture | Robotics engineering, not construction work; the field is hard | none declared | unknown | 2026-09-24 |
| [Navigation2](https://github.com/ros-navigation/navigation2) | Navigation and path planning stack for mobile robots | Assumes a known map and an engineered environment | custom | C++ | 2026-09-22 |
| [grbl](https://github.com/gnea/grbl) | Motion control firmware for CNC machines | Firmware for hobby and small machines | custom | C | 2024-06-12 |
| [LinuxCNC](https://github.com/LinuxCNC/linuxcnc) | Machine control for CNC fabrication equipment | Shop fabrication rather than site work | GPL-2.0 | Python | 2026-09-24 |
| [Universal Gcode Sender](https://github.com/winder/Universal-G-Code-Sender) | Sends G-code to CNC controllers | Shop tooling; not a production control system | GPL-3.0 | Java | 2026-09-12 |

### Standards, schemas and public data

Not software, but you will need them, and they belong in the same bookmarks.

| Resource | What it is | Caveat |
| --- | --- | --- |
| [openLCA](https://www.openlca.org/) | Life cycle assessment software, open source but distributed outside GitHub | Result quality depends on the database you licence, not on the software |
<!-- end:index -->

## What open source does not give you yet

Worth saying plainly, because the gaps are where the commercial software earns its money:

- **No construction-native ERP.** General ERPs can be shaped into job costing, but AIA-style billing, retainage,
  WIP schedules and cost-to-complete discipline are not there out of the box.
- **No credible open source quantity takeoff with pricing.** You can extract quantities from a model, and there
  are good tools for that. Turning quantities into a priced estimate with means, methods and risk is still a
  commercial product or a spreadsheet.
- **No claim-grade CPM.** Gantt tools exist; float analysis, time impact analysis and contemporaneous delay
  records are not open source.
- **No document control.** Archives and wikis are not transmittals, revisions and approval workflows. EDMS
  projects get close and then are not construction-aware.
- **Thin construction-specific analytics.** Reality capture, GIS and ML tooling are strong; the layers that turn
  them into a progress measurement or a productivity read still mostly get written in-house.

That list is also a fair summary of where a small team could contribute something genuinely useful.

## How to evaluate one of these properly

Before you put any of it on a live job, answer these five questions:

1. **Is it somebody's day job?** A project with one maintainer and no employer behind it is a project you are
   now co-maintaining.
2. **What is the licence, and what does it oblige you to do?** Check the licence file itself, not just the
   SPDX badge.
3. **Can you get your data out?** Ask what the export looks like before you put project data in.
4. **What does it cost to run?** A server, a database and a GPU are operational commitments, not downloads.
5. **Who supports it when it breaks on a Friday?** If the answer is "the community", plan for the delay.

## How this list is maintained

```bash
python3 scripts/refresh.py          # re-verify every entry against the GitHub API and rebuild the index
python3 scripts/validate.py         # check the sources file, the index and this README agree
```

`scripts/refresh.py` is the only thing that writes the index block above: it queries the GitHub API for each
project and refuses to invent metadata. Entries that stop answering stay listed, visibly, under
*Not verifiable right now* rather than being quietly deleted. A scheduled workflow re-runs the refresh weekly.

## Contributing

Add a row to `sources/tools.csv` and run the refresh. Rules:

- The project must be **verifiable** — a live repository or a real project page.
- The **caveat is mandatory**. If you cannot say what a tool is bad at, you have not used it.
- **No dead projects** without an honest note, no abandonware dressed as active, no "AI-powered" entries with
  nothing behind them.
- **Construction relevance**, not general software: a task tracker qualifies only if you can point at the
  construction workflow it serves.

## Related

- [`constructelligence-lab/construction-data`](https://github.com/constructelligence-lab/construction-data) —
  general construction reference data: cost codes, units, waste factors, glossary, metric formulas.
- [`constructelligence-lab/ai-in-construction`](https://github.com/constructelligence-lab/ai-in-construction) —
  a practical guide to AI in construction: what works, what your data has to look like, and a 90-day plan.

## Licence

The list itself is CC BY 4.0 — use it, adapt it, credit it. The projects listed keep their own licences, which
are shown per row and belong to their authors.

---

*Maintained by [Constructelligence](https://constructelligence.co) — construction cost intelligence for
contractors.*
