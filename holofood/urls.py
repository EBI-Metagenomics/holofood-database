"""HolofoodDatabase URL Configuration

   Copyright EMBL-European Bioinformatics Institute, 2022

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.


The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, include, get_resolver
from django.views.defaults import page_not_found

from holofood.api import api
from holofood.export import export_api
from holofood.views import (
    SampleListView,
    SampleDetailView,
    AnalysisSummaryDetailView,
    AnalysisSummaryListView,
    HomeView,
    GenomeCatalogueView,
    GenomeCataloguesView,
    ViralCataloguesView,
    ViralCatalogueView,
    ViralCatalogueFragmentView,
    ViralSequenceAnnotationView,
    GlobalSearchView,
    AnimalListView,
    AnimalDetailView,
    ViralCataloguesEmptyStateView,
    GenomeDetailView,
)

admin.site.site_header = "HoloFood Data Portal Admin"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("admin/", admin.site.urls),
    path("404/", page_not_found, {"exception": Exception()}),
    path("martor/", include("martor.urls")),
    path("samples/", SampleListView.as_view(), name="samples_list"),
    path("sample/<str:pk>", SampleDetailView.as_view(), name="sample_detail"),
    path("animals/", AnimalListView.as_view(), name="animals_list"),
    path("animal/<str:pk>", AnimalDetailView.as_view(), name="animal_detail"),
    path(
        "analysis-summaries/",
        AnalysisSummaryListView.as_view(),
        name="analysis_summary_list",
    ),
    path(
        "analysis-summary/<str:slug>",
        AnalysisSummaryDetailView.as_view(),
        name="analysis_summary_detail",
    ),
    path(
        "genome-catalogue/<str:pk>",
        GenomeCatalogueView.as_view(),
        name="genome_catalogue",
    ),
    path("genome-catalogues", GenomeCataloguesView.as_view(), name="genome_catalogues"),
    path(
        "genome-catalogue/<str:catalogue_pk>/<str:pk>",
        GenomeDetailView.as_view(),
        name="genome_detail",
    ),
    path(
        "viral-catalogue/<str:pk>",
        ViralCatalogueView.as_view(),
        name="viral_catalogue",
    ),
    path(
        "viral-catalogue/<str:pk>/<str:viral_fragment_pk>",
        ViralCatalogueFragmentView.as_view(),
        name="viral_catalogue_fragment",
    ),
    path("viral-catalogues", ViralCataloguesView.as_view(), name="viral_catalogues"),
    path(
        "viral-catalogues-redirect",
        ViralCataloguesEmptyStateView.as_view(),
        name="viral_catalogues_empty_state",
    ),
    path("search/", GlobalSearchView.as_view(), name="global_search"),
    path("api/", api.urls),
    path("export/", export_api.urls),
    path(
        "viral-sequence-gff/<str:pk>",
        ViralSequenceAnnotationView.as_view(),
        name="viral_fragment_gff",
    ),
]

if settings.DEBUG:
    urlpatterns += [
        path("__debug__/", include("debug_toolbar.urls")),
    ]


urlpatterns += staticfiles_urlpatterns()
