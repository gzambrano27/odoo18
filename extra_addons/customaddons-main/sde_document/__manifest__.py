# -*- coding: utf-8 -*-
{
    "name": "SSE – Solicitud de Salida de Equipos",
    "version": "18.0.1.0",
    "summary": "Gestión de solicitudes de salidas de equipos electronicos con Qr",
    "author": "MATHEU ZAMBRANO",
    "category": "Human Resources",
    "depends": ["base", "mail", "hr"],
    "data": [
        "security/sse_security.xml",
        "security/ir.model.access.csv",
        "data/sse_sequence.xml",
        "data/report_sse_document.xml",
        "views/sse_document_views.xml",
        "views/sse_document_menu.xml",
    ],
    "images": [
        "static/description/logo.png",
        "static/description/icon.png",
    ],
    "application": False,
    "license": "LGPL-3",
}
