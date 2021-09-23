---
layout: default
title: Adding Runbook documentation
lcb: "{"
---
## Jekyll setup

The runbooks respository generates static sites via GitHub Pages and [Jekyll](https://jekyllrb.com/). There is a
[Jekyll cheatsheet](https://devhints.io/jekyll) you may find handy.

This [article](https://help.github.com/articles/setting-up-your-github-pages-site-locally-with-jekyll/) is helpful to set up your local environment.
<br/>Alternatively, if you have docker installed,
from the root of the documentation repository, you can run the site by entering the following command `docker run -v $PWD:/srv/jekyll -p 4000:4000 -w /srv/jekyll jekyll/jekyll jekyll serve`.  The site can then be accessed at http://localhost:4000/


## How to add an IBM Cloud runbook

1. Create a markdown file (.md) for your runbook and place it under the directory: `/docs/runbooks/component_name/`
    1. Replace the `component_name` with the component name for which the runbook is being added.
    2. Make sure you add the metadata to describe the runbook. The required metadata can be found in the [runbook templates](#follow-the-runbook-templates) below. This is used to populate lists of runbooks and to help searching for runbooks.
    3. The content can be specified using just markdown language. A basic markdown tutorial can be found [here](http://markdowntutorial.com/). If markdown extensions are used, please follow the [Kramdown extended syntax](http://kramdown.gettalong.org/syntax.html).
    4. If the runbook is already developed in html format, then the html can be embedded directly into the markdown file.
2. After adding/updating markdown files for runbooks, run the script to update related json files:
   * `python3 script/OSSRunbookJsonGenerator.py --runbooks`
   * Pre-requirements:
     * Python3
        - `brew install python3`
     * PIP installation
        - `https://www.geeksforgeeks.org/how-to-install-pip-in-macos/`
     * YMAL
        -  `pip install pyyaml`

This script will generate json files for each component, which will be used for searching runbooks. Json files generated are placed under the directory: `/assets/json/`, with names in the format: `component_name-runbook-list.json`.
3. Update the `runbooklist` dropdown-menu in `_includes/docs-toc.html` to include the component when a new component is added:  
`<li><a href="{{ site.baseurl }}/docs/runbooks/runbooks.html#component_name">component_name</a></li>`  
Replace the `component_name` with the name of the new added component.
4. Note:  Always use the _{{ page.lcb }}{ site.baseurl }}_ variable instead of a static path when referencing files within the repo such as images.
        ```![SSH image]({{ page.lcb }}{site.baseurl}}/docs/runbooks/doctor/images/SSH.png){:width="680px" height="288px"} ```



## Follow the runbook templates
When adding a runbook, follow one of the following example tempates:

* For PagerDuty alerts: [PagerDuty runbook template](./pd_runbook_template.html).
* For OSS DevOps Platform alerts: [OSS DevOps Alert runbook template](./oss_alert_runbook_template.html).
* For informational runbooks: [Informational runbook template](./info_runbook_template.html).
* For troubleshooting runbooks: [Troubleshooting runbook template](./troubleshooting_runbook_template.html).

## Content referencing for reusable content based on target build

In situations where you have content that references URLs, contact names, slack channels, etc that would differ between
IBM and Wanda, you can use [Jekyll data files](https://jekyllrb.com/docs/datafiles/).

To add content references of the form `{{ page.lcb }}{site.data.ibm.conrefs.keyword}}`:

1. Create conrefs.yml within both the _data/ibm and _data/wanda folders as an example.
2. Contents in conrefs.yml should take the following format:
```
keyword:
  text to display
another_keyword:
  more text to display
```
3. When writing markdown, a content reference can be created by using `{{ page.lcb }}{site.data[site.target].conrefs.keyword}}` which in this example will display "text to display".

    *site.target* would be set to either ibm or wanda based on the target audience we are building the docs for.  In the sample above the
    content reference would use the conrefs.yml file from the corresponding ibm or wanda folder under _data.

## Adding conditional content blocks based on target build

In situations where you have blocks of content within a runbook that would differ between
IBM and Wanda, you can follow the techniques below which use [Jekyll relative includes](https://jekyllrb.com/docs/includes/).

1. Add variable named *target* with value 'ibm' to _config.yml.
2. Add folders named _ibm-includes and _wanda-includes within each component_name folder. When the site build is done for sending docs to Wanda, the *site.target* variable will be changed to 'wanda' and all folders
named _ibm-includes will be excluded from the build.
3. To add content to a markdown page which would be applicable to a specific target only, wrap the content with an
if statement checking the *site.target* variable and use include-relative to include the applicable html or md partial.

    ```
    Using an html partial

    {{ page.lcb }}% if site.target == "ibm" %}
      {{ page.lcb }}% include_relative _ibm-includes/xen7-migration.html %}
    {{ page.lcb }}% endif %}


    Using a markdown partial

    {{ page.lcb }}% if site.target == "ibm" %}
      {{ page.lcb }}% capture my_include %}
        {{ page.lcb }}% include_relative _ibm-includes/xen7-migration.md %}
      {{ page.lcb }}% endcapture %}
      {{ page.lcb }}{ my_include | markdownify }}
    {{ page.lcb }}% endif %}
    ```
4. To add content sections which differ between targets (e.g. ibm or wanda), use site.target to include the applicable partial from either
the ibm-includes or wanda-includes folders.

    ```
    {{ page.lcb }}% capture my_include %}
        {{ page.lcb }}% include_relative _{{ page.lcb }}{ site.target }}-includes/special.md %}
    {{ page.lcb }}% endcapture %}
    {{ page.lcb }}{ my_include | markdownify }}
    ```
