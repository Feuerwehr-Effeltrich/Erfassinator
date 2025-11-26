"""Dummy backend that simulates a website for testing."""

import time
import requests
import bs4
import json
import re
from typing import Optional, Any
from dataclasses import dataclass
from abc import ABC, abstractmethod

@dataclass
class DataEntry:
    """Represents a data entry from the website."""

    id: int
    title: str
    date: str
    status: str
    description: str

class Backend(ABC):
    authenticated: bool
    username: Optional[str]

    @abstractmethod
    def login(self, username: str, password: str) -> bool:
        ...

    @abstractmethod
    def logout(self) -> None:
        ...

    @abstractmethod
    def fetch_data(self) -> list[DataEntry]:
        ...

    @abstractmethod
    def apply_action(self, entry_id: int) -> bool:
        ...

class DummyBackend(Backend):
    """Mock backend that simulates website authentication and data fetching."""

    def __init__(self):
        self.authenticated = False
        self.username: Optional[str] = None

    def login(self, username: str, password: str) -> bool:
        """Simulate login. Accepts 'admin'/'admin' or 'user'/'password'."""
        time.sleep(0.5)  # Simulate network delay

        valid_credentials = [
            ("admin", "admin"),
            ("user", "password"),
        ]

        if (username, password) in valid_credentials:
            self.authenticated = True
            self.username = username
            return True
        return False

    def logout(self):
        """Logout the current user."""
        self.authenticated = False
        self.username = None

    def fetch_data(self) -> list[DataEntry]:
        """Fetch dummy data entries."""
        if not self.authenticated:
            raise PermissionError("Not authenticated")

        time.sleep(0.3)  # Simulate network delay

        return [
            DataEntry(
                1, "Einsatz Brand", "2024-01-15", "Ausstehend", "Kleinbrand im Keller"
            ),
            DataEntry(
                2, "Technische Hilfe", "2024-01-16", "Ausstehend", "Ölspur auf Fahrbahn"
            ),
            DataEntry(
                3, "Einsatz Rettung", "2024-01-17", "Ausstehend", "Person eingeklemmt"
            ),
            DataEntry(4, "Fehlalarm", "2024-01-18", "Ausstehend", "BMA ausgelöst"),
            DataEntry(
                5, "Einsatz Brand", "2024-01-19", "Ausstehend", "Mülltonnenbrand"
            ),
        ]

    def apply_action(self, entry_id: int) -> bool:
        """Apply action to a single entry. Returns success status."""
        if not self.authenticated:
            raise PermissionError("Not authenticated")

        time.sleep(0.2)  # Simulate processing
        return True

class FWPortalBackend(Backend):
    url = "https://live.fwportal.de"

    def __init__(self):
        self.authenticated = False
        self.username: Optional[str] = None
        self.session = requests.Session()

    def login(self, username: str, password: str) -> bool:
        homepage = self.session.get(self.url)
        parsed = bs4.BeautifulSoup(homepage.text, features="html.parser")
        infield = parsed.find("input", attrs={"name": "__RequestVerificationToken"})
        if not infield:
            return False
        verificationToken = str(infield.attrs["value"])

        response = self.session.post(f"{self.url}/Account/LogOn", data={
            "__RequestVerificationToken": verificationToken,
            "UserName": username,
            "Password": password,
            "AngemeldetBleiben": "false"
        })

        self.authenticated = response.status_code == 200 and "ungelesene Nachrichten" in self.session.get(self.url).text
        return self.authenticated

    def logout(self):
        """Logout the current user."""
        self.authenticated = False
        self.username = None
        self.session.get(f"{self.url}/Account/LogOff")

    def fetch_data(self) -> list[DataEntry]:
        """Fetch dummy data entries."""
        if not self.authenticated:
            raise PermissionError("Not authenticated")

        response = self.session.post(f"{self.url}/Einsatz/EinsatzGridAjax")

        data: list[Any] = json.loads(response.text)["Data"]

        return list(map(lambda x: DataEntry(
                id = x["EinsatzberichtID"],
                title = x["Stichwort"],
                date = x["BeginnDatumText"],
                status = x["GesamtStatus"],
                description = x["Kurzbeschreibung"]
            ), data))

    def apply_action(self, entry_id: int) -> bool:
        """Apply action to a single entry. Returns success status."""
        if not self.authenticated:
            raise PermissionError("Not authenticated")

        response = self.session.get(f"{self.url}/Einsatz/GetUpdateEinsatzberichtStatus/{entry_id}", params={
            "stat": 0 # Erfassen
        })

        if response.status_code != 200:
            return False

        parsed = bs4.BeautifulSoup(response.text, features="html.parser")
        infield = parsed.find("input", attrs={"name": "__RequestVerificationToken"})
        if not infield:
            return False
        verificationToken = str(infield.attrs["value"])
        search = re.search(r'organisationid=(\d+)', response.text)
        if not search:
            return False
        orgid = search.group(1)

        response = self.session.post(f"{self.url}/einsatz/saveupdateeinsatzberichtstatus/{entry_id}", params={
            "status": 100, # Bestätigen
            "organisationid": orgid
        }, data={
            "__RequestVerificationToken": verificationToken,
            "UpdateStatusBemerkung": "",
            "X-Requested-With": "XMLHttpRequest",
        })

        return response.status_code == 200
