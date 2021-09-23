SHELL := /bin/bash
RB_DIR := docs/runbooks
SITE_DIR := _site
md_files := $(wildcard $(RB_DIR)/*.md)
json_files := $(wildcard $(SITE_DIR)/assets/json/*.json)
checkkeysprog :="./script/checkkeys.py"
templatekeys :="./script/runbooks_template_keys.json"


define do_yamllint
	grep -B50 "\-\-\-" $(file) | grep -vE "\b\-\-\b" > tmp.yml;
	yamllint tmp.yml> /dev/null &2>1;
endef

define do_jsonlint
	jsonlint $(file);
endef

define do_checkkeys
	echo "Check keys in $(file)"
	python $(checkkeysprog) $(file) $(templatekeys) || exit;
endef


all: clean verify_metadata yaml_lint jekyll html_lint json_lint check_keys check_json_generator
.PHONY: all

define pretty_output
	echo -e "\n\n\n\n\e[32m$(1)\e[0m"
endef

clean:
	$(call pretty_output, "Run Clean to remove this directory: $(SITE_DIR)")
	rm -rf $(SITE_DIR)

verify_metadata:
	$(call pretty_output, "Verify Metadata")
	bash script/verify_metadata.sh

yaml_lint: $(md_files)
	$(call pretty_output, "Run Yml Linter")
	$(foreach file,$(md_files),$(do_yamllint))

jekyll:
	$(call pretty_output, "Run jekyll")
	jekyll build --source . --destination $(SITE_DIR)

html_lint: jekyll
	$(call pretty_output, "Run HTML Linter")
	htmlproofer --disable-external --empty-alt-ignore --allow-hash-href --file-ignore "_site/tools.html,_site/view.html,_site/docs/runbooks/images/repo-jenkins-fileserver.html" $(SITE_DIR)

json_lint:
	$(call pretty_output, "Run Json Linter")
	$(foreach file,$(json_files),$(do_jsonlint))

check_keys: $(md_files)
	$(call pretty_output, "Run Check Keys Test")
	@$(foreach file,$(md_files),$(do_checkkeys))

# This check verifies the runbook json files will generate... If it fails that means
# runbooks WON'T generate on the next deployment of the Runbook webpage.
check_json_generator:
	$(call pretty_output, "Show missing Values in Metadata")
	python script/RunbookJsonGenerator.py --missing
