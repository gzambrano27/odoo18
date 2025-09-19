# -*- coding: utf-8 -*-
{
    "name": "Gantt View PRO",
    "version": "18.0.1.0",
    "summary": "Manage and visualise your projects with the fastest Gantt chart on the web.",
    "author": "Guillermo Zambrano",
    "website": "http://www.gpsgroup.ec",
    "category": "Project",
    "license": "LGPL-3",
    "depends": ["base", "web", "project", "hr", "hr_timesheet"],
    "data": [
        "security/project_security.xml",
        "security/ir.model.access.csv",
        "views/res_config_settings_views.xml",
        "views/project_views.xml",
        "wizard/import_mpp_views.xml",
    ],
    "demo": ["demo/demo.xml"],
    "images": [
        "images/banner.png",
        "images/main_screenshot.png",
        "images/reschedule.gif",
    ],
    "assets": {
        "web.assets_backend": [
            "/bryntum_gantt/static/src/js/error_service.esm.js",
            "/bryntum_gantt/static/src/js/main.js",
            "/bryntum_gantt/static/src/css/main.css",
        ]
    },
    "installable": True,
    "application": True,
    "post_init_hook": "post_init_hook",
    "price": 890.00,
    "currency": "USD",
}
