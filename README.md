# Chemical Equipment Visualizer

A full-stack application for visualizing and analyzing chemical equipment data. The system consists of three main components: a Django REST API backend, a React web frontend, and a PyQt5 desktop application.

##  Project Overview

The Chemical Equipment Visualizer allows users to:
- Upload and manage chemical equipment CSV data
- Visualize equipment metrics through interactive charts and dashboards
- Generate PDF reports with equipment summaries
- Access data via REST API endpoints
- View real-time updates with a responsive web interface

##  Architecture

### System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                        Chemical Equipment Visualizer                 │
└─────────────────────────────────────────────────────────────────────┘

                              ┌──────────────────┐
                              │                  │
                              │   SQLite DB      │
                              └────────┬─────────┘
                                       │
                ┌──────────────────────┼──────────────────────┐
                │                      │                      │
        ┌───────▼────────┐    ┌────────▼────────┐    ┌──────▼──────────┐
        │   Django REST  │    │  File Storage   │    │  Media Server   │
        │   API Backend  │    │  (CSV, PDF)     │    │  (Static Files) │
        │   (Port 8000)  │    │                 │    │                 │
        └───────┬────────┘    └─────────────────┘    └─────────────────┘
                │
        ┌───────┴─────────────────────────────┬──────────────────┐
        │                                     │                  │
        │            REST Endpoints           │                  │
        │   /api/equipment/                   │                  │
        │   /api/upload/                      │                  │
        │   /api/charts/                      │                  │
        │                                     │                  │
        └───────┬─────────────────────────────┘                  │
                │                                                │
        ┌───────▼───────────┐                         ┌──────────▼──────────┐
        │  React Web App    │                         │  PyQt5 Desktop App  │
        │  (Port 3000)      │                         │  (Local/Standalone) │
        │                   │                         │                     │
        │ ✓ Charts          │                         │ ✓ CSV Upload        │
        │ ✓ Dashboards      │                         │ ✓ Data Visualization│
        │ ✓ File Upload     │                         │ ✓ PDF Export        │
        │ ✓ Reports         │                         │ ✓ Direct API Access │
        └───────────────────┘                         └─────────────────────┘
```

### Component Details

#### Backend (Django REST Framework)
- **Framework**: Django 5.2.10
- **API**: Django REST Framework 3.16.1
- **Database**: SQLite (configurable to PostgreSQL)
- **Port**: 8000
- **Key Features**:
  - Equipment data models and management
  - CSV file upload and parsing
  - PDF report generation (ReportLab)
  - Data visualization endpoints (Matplotlib, Pandas)
  - CORS support for web frontend

#### Frontend (React)
- **Framework**: React 19.2.4
- **Charting**: Chart.js with react-chartjs-2
- **Port**: 3000
- **Key Features**:
  - Interactive equipment charts
  - Summary cards and statistics
  - File upload interface
  - History table for equipment data
  - Real-time data loading indicators

#### Desktop Application (PyQt5)
- **Framework**: PyQt5 5.15.11
- **Port**: Connects to API on port 8000
- **Key Features**:
  - CSV file selection and upload
  - Local data visualization
  - PDF export functionality
  - Direct backend API communication

##  Setup Instructions

### Prerequisites

Before starting, ensure you have:
- **Python 3.10+** installed
- **Node.js 16+** and **npm** installed
- **Git** for version control

### 1. Backend Setup (Django)

Navigate to the backend directory:

```bash
cd backend
```

Create and activate a virtual environment:

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/macOS
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run database migrations:

```bash
python manage.py migrate
```

Create a superuser (admin) account:

```bash
python manage.py createsuperuser
```

Start the development server:

```bash
python manage.py runserver
```

The API will be available at: `http://localhost:8000`

**API Documentation**: Visit `http://localhost:8000/api/` for the browsable API interface.

---

### 2. Frontend Setup (React)

In a new terminal, navigate to the web directory:

```bash
cd web/visualizer
```

Install dependencies:

```bash
npm install
```

Start the development server:

```bash
npm start
```

The web application will open automatically at: `http://localhost:3000`

**Build for production**:

```bash
npm run build
```

---

### 3. Desktop Application Setup (PyQt5)

In a new terminal, navigate to the desktop directory:

```bash
cd desktop
```

Ensure the backend virtual environment is still active or install dependencies:

```bash
pip install PyQt5 requests matplotlib
```

Run the desktop application:

```bash
python app.py
```

Make sure the Django backend is running on `http://127.0.0.1:8000` before launching the desktop app.

---

##  Project Structure

```
chemical-equipment-visualizer/
│
├── backend/                          # Django REST API
│   ├── config/                       # Django project settings
│   │   ├── settings.py               # Main settings
│   │   ├── urls.py                   # URL routing
│   │   ├── wsgi.py                   # WSGI configuration
│   │   └── asgi.py                   # ASGI configuration
│   │
│   ├── equipment/                    # Main Django app
│   │   ├── models.py                 # Database models
│   │   ├── views.py                  # API views
│   │   ├── urls.py                   # App routing
│   │   ├── admin.py                  # Admin interface
│   │   ├── serializers.py            # DRF serializers
│   │   ├── pdf.py                    # PDF generation
│   │   ├── utils.py                  # Utility functions
│   │   └── migrations/               # Database migrations
│   │
│   ├── manage.py                     # Django CLI
│   ├── requirements.txt              # Python dependencies
│   ├── runtime.txt                   # Python version (deployment)
│   ├── render.yaml                   # Render.com config (deployment)
│   └── db.sqlite3                    # SQLite database
│
├── web/                              # React Frontend
│   └── visualizer/
│       ├── public/                   # Static assets
│       │   ├── index.html
│       │   └── favicon.ico
│       │
│       ├── src/                      # React source code
│       │   ├── App.js                # Main app component
│       │   ├── index.js              # Entry point
│       │   ├── api.js                # API utilities
│       │   ├── App.css               # Global styles
│       │   └── components/           # React components
│       │       ├── Upload.js
│       │       ├── EquipmentChart.js
│       │       ├── HistoryTable.js
│       │       ├── SummaryCards.js
│       │       └── Loading.js
│       │
│       ├── package.json              # Dependencies & scripts
│       └── vercel.json               # Vercel deployment config
│
├── desktop/                          # PyQt5 Desktop App
│   └── app.py                        # Main desktop application
│
└── README.md                         # Project documentation
```

---

##  API Endpoints

### Equipment Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/equipment/` | List all equipment |
| POST | `/api/equipment/` | Create new equipment |
| GET | `/api/equipment/{id}/` | Get specific equipment |
| PUT | `/api/equipment/{id}/` | Update equipment |
| DELETE | `/api/equipment/{id}/` | Delete equipment |

### Upload Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/upload/` | Upload CSV file |
| GET | `/api/upload/history/` | View upload history |

### Chart/Report Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/charts/` | Get chart data |
| POST | `/api/reports/generate/` | Generate PDF report |

---
## Implementation
<img width="1909" height="864" alt="image" src="https://github.com/user-attachments/assets/cc13539e-8178-4dfd-b145-33b6a7de0122" />
<img width="1873" height="860" alt="image" src="https://github.com/user-attachments/assets/00740f65-91c3-4c53-acb0-2ff8c08eb5be" />
<img width="561" height="792" alt="image" src="https://github.com/user-attachments/assets/aeb50214-e6ed-48f2-a0e9-bb27a0fb2a49" />
<img width="976" height="594" alt="image" src="https://github.com/user-attachments/assets/a815b08c-ba36-49a3-8361-2241b4c868f2" />
<img width="1686" height="717" alt="image" src="https://github.com/user-attachments/assets/9f3b0121-5637-406f-898b-d9f06c0d375b" />


##  Development Guide

### Backend Development

**Add a new model**:
1. Edit `backend/equipment/models.py`
2. Create migration: `python manage.py makemigrations`
3. Apply migration: `python manage.py migrate`

**Create a new API endpoint**:
1. Update `views.py` with new viewset
2. Register in `serializers.py`
3. Add URL pattern in `urls.py`

### Frontend Development

**Add a new component**:
1. Create file in `web/visualizer/src/components/`
2. Import and use in `App.js`
3. Style with CSS or inline styles

**Update API calls**:
- Modify endpoints in `web/visualizer/src/api.js`
- Update React components to consume new data

---

##  Deployment

### Deploy Backend to Render.com

1. Push code to GitHub
2. Connect repository to Render
3. Use `render.yaml` for configuration
4. Set environment variables (SECRET_KEY, DEBUG, ALLOWED_HOSTS)

### Deploy Frontend to Vercel

1. Push code to GitHub
2. Connect repository to Vercel
3. Use `vercel.json` for build configuration
4. Set API endpoint environment variable

### Deploy Desktop App

- Package with PyInstaller:
  ```bash
  pip install pyinstaller
  pyinstaller --onefile app.py
  ```

---

##  Environment Variables

Create a `.env` file in the backend directory:

```
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
CORS_ALLOWED_ORIGINS=http://localhost:3000
```

---

##  Features

-  CSV file upload and parsing
-  Equipment data management
-  Interactive charts and visualizations
-  PDF report generation
-  REST API with CORS support
-  Admin dashboard (Django admin)
-  Responsive web interface
-  Desktop application support
-  Real-time data updates

---

##  Troubleshooting

### Backend won't start
- Ensure virtual environment is activated
- Run migrations: `python manage.py migrate`
- Check if port 8000 is available

### Frontend won't connect to API
- Verify backend is running on `http://localhost:8000`
- Check CORS settings in `backend/config/settings.py`
- Clear browser cache and restart dev server

### Desktop app shows connection error
- Ensure Django backend is running
- Verify API_BASE URL in `app.py` matches your backend
- Check firewall settings

---

##  License

This project is open source and available under the MIT License.

---

##  Author

**Shrishti Singh**

GitHub: [@ShrishtiSingh26](https://github.com/ShrishtiSingh26)

---

##  Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

##  Support

For issues, questions, or suggestions, please open an issue on GitHub:
[chemical-equipment-visualizer/issues](https://github.com/ShrishtiSingh26/chemical-equipment-visualizer/issues)
