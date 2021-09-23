var ToC = "<nav role='navigation' class='bs-docs-sidebar'>" +
            "<ul id='toc-sidebar' class='nav nav-stacked'>";

if ($("#content-loc").find("h1").length > 1){
    var el, title, link;
    $("h1").each(function() {
        el = $(this);
        title = el.text();
        link = "#" + (el.attr("id") ? el.attr("id") : "");
        var newline = "<li><a href='"+link+"'>"+title+"</a><ul class='nav nav-stacked'>"
        el.nextUntil("h1", "h2").each(function(){
            el = $(this);
            title = el.text();
            link = "#" + el.attr("id");
            newline += "<li><a href='"+link+"'>"+title+"</a></li>"
        });
        newline += "</ul></li>"

        ToC += newline;
    });
}
else{
    var el, title, link;
    $("h2").each(function() {
        el = $(this);
        title = el.text();
        link = "#" + (el.attr("id") ? el.attr("id") : "");
        var newline = "<li><a href='"+link+"'>"+title+"</a><ul class='nav nav-stacked'>"
        el.nextUntil("h2", "h3").each(function(){
            el = $(this);
            title = el.text();
            link = "#" + el.attr("id");
            newline += "<li><a href='"+link+"'>"+title+"</a></li>"
        });
        newline += "</ul></li>"

        ToC += newline;
    });
}

ToC +=
   "</ul>" +
  "</nav>";
$("#tableofcontentsholder").prepend(ToC);

$('body').scrollspy({
    target: '.bs-docs-sidebar',
    offset: 40
});

$("#toc-sidebar").affix({
    offset: {
      top: 60
    }
});
