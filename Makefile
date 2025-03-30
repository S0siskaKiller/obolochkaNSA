PYTHON = python3
PYINSTALLER = pyinstaller
SCRIPT = оболочкаНСА.py
DIST_DIR = dist
BUILD_DIR = build
EXECUTABLE = nsa
INSTALL_DIR = /usr/local/bin 

all: build

build:
	$(PYINSTALLER) --onefile --windowed --name $(EXECUTABLE) --distpath $(DIST_DIR) --workpath $(BUILD_DIR) $(SCRIPT)

install: build
	sudo mkdir -p $(INSTALL_DIR) 
	sudo cp dist/nsa /usr/local/bin/nsa
	sudo chmod +x $(INSTALL_DIR)/$(EXECUTABLE)
	@echo "Installed $(EXECUTABLE) to $(INSTALL_DIR)"


clean:
	rm -rf $(DIST_DIR) $(BUILD_DIR) __pycache__

run:
	$(PYTHON) $(SCRIPT)

deps:
	pip install alsaaudio psutil pyinstaller

.PHONY: all build clean run deps install
