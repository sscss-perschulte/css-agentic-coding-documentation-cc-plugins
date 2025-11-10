#!/usr/bin/env python3
"""
Google Docs Document Filler

Dieses Script ermöglicht das Befüllen von Google Docs Dokumenten mit Inhalten.
"""

import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import pickle

# Scopes für Google Docs API
SCOPES = ['https://www.googleapis.com/auth/documents']


class GoogleDocsManager:
    """Manager für Google Docs Operationen"""

    def __init__(self, credentials_file='credentials.json'):
        """
        Initialisiert den Google Docs Manager

        Args:
            credentials_file: Pfad zur OAuth 2.0 Client ID JSON-Datei
        """
        self.credentials_file = credentials_file
        self.creds = None
        self.service = None
        self._authenticate()

    def _authenticate(self):
        """Authentifizierung mit Google API"""
        # Token aus pickle-Datei laden, falls vorhanden
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                self.creds = pickle.load(token)

        # Wenn keine gültigen Credentials vorhanden, neue anfordern
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_file, SCOPES)
                self.creds = flow.run_local_server(port=0)

            # Token speichern für zukünftige Verwendung
            with open('token.pickle', 'wb') as token:
                pickle.dump(self.creds, token)

        self.service = build('docs', 'v1', credentials=self.creds)

    def create_document(self, title):
        """
        Erstellt ein neues Google Docs Dokument

        Args:
            title: Titel des Dokuments

        Returns:
            Document ID des erstellten Dokuments
        """
        try:
            document = self.service.documents().create(body={'title': title}).execute()
            doc_id = document.get('documentId')
            print(f'Dokument erstellt mit ID: {doc_id}')
            print(f'URL: https://docs.google.com/document/d/{doc_id}/edit')
            return doc_id
        except HttpError as error:
            print(f'Ein Fehler ist aufgetreten: {error}')
            return None

    def append_text(self, document_id, text):
        """
        Fügt Text am Ende des Dokuments hinzu

        Args:
            document_id: ID des Google Docs Dokuments
            text: Text, der hinzugefügt werden soll
        """
        try:
            requests = [
                {
                    'insertText': {
                        'location': {
                            'index': 1,
                        },
                        'text': text
                    }
                }
            ]

            result = self.service.documents().batchUpdate(
                documentId=document_id, body={'requests': requests}).execute()
            print(f'Text erfolgreich hinzugefügt')
            return result
        except HttpError as error:
            print(f'Ein Fehler ist aufgetreten: {error}')
            return None

    def insert_text_at_position(self, document_id, text, index):
        """
        Fügt Text an einer bestimmten Position ein

        Args:
            document_id: ID des Google Docs Dokuments
            text: Text, der eingefügt werden soll
            index: Position im Dokument (1 = Anfang)
        """
        try:
            requests = [
                {
                    'insertText': {
                        'location': {
                            'index': index,
                        },
                        'text': text
                    }
                }
            ]

            result = self.service.documents().batchUpdate(
                documentId=document_id, body={'requests': requests}).execute()
            print(f'Text an Position {index} eingefügt')
            return result
        except HttpError as error:
            print(f'Ein Fehler ist aufgetreten: {error}')
            return None

    def replace_text(self, document_id, find_text, replace_text):
        """
        Ersetzt Text im Dokument

        Args:
            document_id: ID des Google Docs Dokuments
            find_text: Text, der gesucht werden soll
            replace_text: Text, der als Ersatz eingefügt werden soll
        """
        try:
            requests = [
                {
                    'replaceAllText': {
                        'containsText': {
                            'text': find_text,
                            'matchCase': False
                        },
                        'replaceText': replace_text
                    }
                }
            ]

            result = self.service.documents().batchUpdate(
                documentId=document_id, body={'requests': requests}).execute()
            print(f'Text "{find_text}" ersetzt durch "{replace_text}"')
            return result
        except HttpError as error:
            print(f'Ein Fehler ist aufgetreten: {error}')
            return None

    def add_formatted_text(self, document_id, text, bold=False, italic=False,
                          font_size=11, index=1):
        """
        Fügt formatierten Text hinzu

        Args:
            document_id: ID des Google Docs Dokuments
            text: Text, der hinzugefügt werden soll
            bold: Text fett formatieren
            italic: Text kursiv formatieren
            font_size: Schriftgröße
            index: Position im Dokument
        """
        try:
            requests = [
                {
                    'insertText': {
                        'location': {
                            'index': index,
                        },
                        'text': text
                    }
                }
            ]

            # Formatierung hinzufügen
            text_style = {}
            if bold:
                text_style['bold'] = True
            if italic:
                text_style['italic'] = True
            if font_size:
                text_style['fontSize'] = {
                    'magnitude': font_size,
                    'unit': 'PT'
                }

            if text_style:
                requests.append({
                    'updateTextStyle': {
                        'range': {
                            'startIndex': index,
                            'endIndex': index + len(text)
                        },
                        'textStyle': text_style,
                        'fields': ','.join(text_style.keys())
                    }
                })

            result = self.service.documents().batchUpdate(
                documentId=document_id, body={'requests': requests}).execute()
            print(f'Formatierter Text hinzugefügt')
            return result
        except HttpError as error:
            print(f'Ein Fehler ist aufgetreten: {error}')
            return None

    def get_document_content(self, document_id):
        """
        Liest den Inhalt eines Dokuments

        Args:
            document_id: ID des Google Docs Dokuments

        Returns:
            Dokumentinhalt
        """
        try:
            document = self.service.documents().get(documentId=document_id).execute()
            print(f'Dokument Titel: {document.get("title")}')
            return document
        except HttpError as error:
            print(f'Ein Fehler ist aufgetreten: {error}')
            return None


def main():
    """Beispiel-Verwendung"""
    # Google Docs Manager initialisieren
    manager = GoogleDocsManager()

    # Neues Dokument erstellen
    doc_id = manager.create_document('Mein Test-Dokument')

    if doc_id:
        # Text hinzufügen
        manager.append_text(doc_id, 'Hallo Welt!\n\n')

        # Formatierten Text hinzufügen
        manager.add_formatted_text(
            doc_id,
            'Dies ist fetter Text\n\n',
            bold=True,
            font_size=14,
            index=1
        )

        # Platzhalter ersetzen (falls vorhanden)
        # manager.replace_text(doc_id, '{{NAME}}', 'Max Mustermann')

        print(f'\nDokument erfolgreich erstellt und befüllt!')
        print(f'Öffne: https://docs.google.com/document/d/{doc_id}/edit')


if __name__ == '__main__':
    main()
