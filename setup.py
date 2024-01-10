from setuptools import setup
from pathlib import Path


long_description = Path(__file__).with_name("README.md").read_text(encoding="utf-8")

setup(
    name="simple_spaced_repetition",
    py_modules=["simple_spaced_repetition"],
    version="0.2.0",
    description="Simple spaced repetition library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/vlopezferrando/simple-spaced-repetition",
    author="Víctor López Ferrando",
    author_email="victor@thediligentdeveloper.com",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Education :: Computer Aided Instruction (CAI)",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
    ],
    keywords="spaced repetition, anki",
    project_urls={
        "Bug Reports": "https://github.com/vlopezferrando/simple-spaced-repetition/issues",
        "Source": "https://github.com/vlopezferrando/simple-spaced-repetition",
        "Used at": "https://python.cards",
    },
)
