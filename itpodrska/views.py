from django.http import HttpResponse

def pocetna(request):
    return HttpResponse("""
    <h1>Aplikacija za IT podršku</h1>
    <p>Dobrodošli u sustav za evidenciju zahtjeva, incidenata, IT opreme, baze znanja i KPI izvještaja.</p>

    <ul>
        <li><a href="/admin/">Django admin</a></li>
    </ul>
    """)