#!/usr/bin/env python3
"""Build .pyz/.pyzw files with all dependencies bundled."""

import zipapp
import shutil
import subprocess
import tempfile
from pathlib import Path


def build_pyz(output_name: str):
    output_file = Path("dist") / output_name
    output_file.parent.mkdir(exist_ok=True)

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)

        # Copy package
        shutil.copytree("erfassinator", temp_path / "erfassinator")

        # Install dependencies
        subprocess.run(
            [
                "uv",
                "pip",
                "install",
                "--target",
                str(temp_path),
                "requests>=2.32.5",
                "beautifulsoup4>=4.12.0",
            ],
            check=True,
            capture_output=True,
        )

        # Create entry point
        (temp_path / "__main__.py").write_text(
            "from erfassinator.main import main\n"
            "if __name__ == '__main__':\n"
            "    main()\n"
        )

        # Create archive
        zipapp.create_archive(
            temp_path,
            target=output_file,
            interpreter="/usr/bin/env python3",
            compressed=True,
        )

        print(f"✓ {output_file} ({output_file.stat().st_size / 1024:.0f} KB)")
        return output_file


if __name__ == "__main__":
    print("Building .pyz files...\n")
    pyz = build_pyz("erfassinator.pyz")
    pyz.chmod(0o755)
    build_pyz("erfassinator.pyzw")
    print("\nDone!")
