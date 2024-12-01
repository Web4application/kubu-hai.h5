{{>head}}

  <div id="dartdoc-main-content" class="main-content">
    {{#defaultPackage}}
      {{>documentation}}
    {{/defaultPackage}}

    {{#localPackages}}
      <section class="summary">
        {{#isFirstPackage}}
          <h2>Libraries</h2>
        {{/isFirstPackage}}
        {{^isFirstPackage}}
          <h2>{{name}}</h2>
        {{/isFirstPackage}}
        <dl>
        {{#defaultCategory.publicLibrariesSorted}}
          {{>library}}
        {{/defaultCategory.publicLibrariesSorted}}
        {{#categoriesWithPublicLibraries}}
          <h3>{{name}}</h3>
          {{#publicLibrariesSorted}}
            {{>library}}
          {{/publicLibrariesSorted}}
        {{/categoriesWithPublicLibraries}}
        </dl>
      </section>
    {{/localPackages}}

  </div> <!-- /.main-content -->

  <div id="dartdoc-sidebar-left" class="sidebar sidebar-offcanvas-left">
    {{>search_sidebar}}
    <h5 class="hidden-xs"><span class="package-name">{{self.name}}</span> <span class="package-kind">{{self.kind}}</span></h5>
    {{>packages}}
  </div>

  <div id="dartdoc-sidebar-right" class="sidebar sidebar-offcanvas-right">
  </div>

{{>footer}}
