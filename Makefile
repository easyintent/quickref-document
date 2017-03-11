
XMLLINT=xmllint
RM=rm -f

SOURCE=quickref.xml
TARGET=quickref.sqlite
SCHEMA=quickref.rng
SCHEMA_FORMAT=--relaxng

.PHONY: all
all: clean validate $(TARGET)

$(TARGET): $(SOURCE)
	./mkquickref.py $(SOURCE) $@

.PHONY: validate
validate: $(SCHEMA) $(SOURCE)
	$(XMLLINT) --noout $(SCHEMA_FORMAT) $(SCHEMA) $(SOURCE)

.PHONY: clean
clean:
	$(RM) $(TARGET)
