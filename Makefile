
XMLLINT=xmllint
RM=rm -f

SOURCE=quickref.xml
TARGET=quickref.sqlite
SCHEMA=quickref.rng

all: clean validate $(TARGET)

$(TARGET): $(SOURCE)
	./mkquickref.py $(SOURCE) $@

validate: $(SCHEMA) $(SOURCE)
	$(XMLLINT) --noout --relaxng $(SCHEMA) $(SOURCE)

clean:
	$(RM) $(TARGET)
