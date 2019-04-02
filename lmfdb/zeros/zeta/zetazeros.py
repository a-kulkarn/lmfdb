import flask
from mpmath import nstr, inf
from sage.all import floor, log
from lmfdb.logger import make_logger
from flask import render_template, request, url_for

ZetaZeros = flask.Blueprint("zeta zeros", __name__, template_folder="templates")
logger = make_logger(ZetaZeros)

from platt_zeros import zeros_starting_at_N, zeros_starting_at_t


@ZetaZeros.route("/")
def zetazeros():
    N = request.args.get("N", None, int)
    t = request.args.get("t", 0, float)
    limit = request.args.get("limit", 100, int)
    if limit > 1000:
        return list_zeros(N=N, t=t, limit=limit)
    else:
        title = "Zeros of $\zeta(s)$"
        bread = [("L-functions", url_for("l_functions.l_function_top_page")),
                 ('Zeros of $\zeta(s)$', ' ')]
        learnmore = [("Completeness of the data",url_for(".extent")),("Source of the data", url_for(".source")),("Reliability of the data", url_for(".reliability"))]
        return render_template('zeta.html', N=N, t=t, limit=limit, title=title, bread=bread, learnmore=learnmore)


@ZetaZeros.route("/Completeness")
def completeness():
    t = 'Completeness of Reimann Zeta Zeros Data$'
    bread = [("L-functions", url_for("l_functions.l_function_top_page")),("Zeros of $\zeta(s)$", url_for(".zetazeros")),('Extent', ' ')]
    return render_template("single.html", kid='dq.zeros.zeta.extent',
                           credit=credit_string, title=t, bread=bread, learnmore=learnmore_list_remove('Completeness'))

@ZetaZeros.route("/Source")
def source():
    t = 'Source of Reimann Zeta Zeros Data'
    bread = [("L-functions", url_for("l_functions.l_function_top_page")),("Zeros of $\zeta(s)$", url_for(".zetazeros")),('Source', ' ')]
    return render_template("single.html", kid='dq.zeros.zeta.source',
                           credit=credit_string, title=t, bread=bread, learnmore=learnmore_list_remove('Source'))

@ZetaZeros.route("/Reliability")
def reliability():
    t = 'Reliability of Riemann Zeta Zeros Data'
    bread = [("L-functions", url_for("l_functions.l_function_top_page")),("Zeros of $\zeta(s)$", url_for(".zetazeros")),('Reliability', ' ')]
    return render_template("single.html", kid='dq.zeros.zeta.reliability',
                           credit=credit_string, title=t, bread=bread, learnmore=learnmore_list_remove('Reliability'))

@ZetaZeros.route("/list")
def list_zeros(N=None,
               t=None,
               limit=None,
               fmt=None,
               download=None):
    if N is None:
        N = request.args.get("N", None, int)
    if t is None:
        t = request.args.get("t", 0, float)
    if limit is None:
        limit = request.args.get("limit", 100, int)
    if fmt is None:
        fmt = request.args.get("format", "plain")
    if download is None:
        download = request.args.get("download", "no")

    if limit < 0:
        limit = 100
    if N is not None:  # None is < 0!! WHAT THE WHAT!
        if N < 0:
            N = 0
    if t < 0:
        t = 0

    if limit > 100000:
        # limit = 100000
        #
        bread = [("L-functions", url_for("l_functions.l_function_top_page")),("Zeros of $\zeta(s)$", url_for(".zetazeros"))]
        return render_template('single.html', title="Too many zeros", bread=bread, kid = "dq.zeros.zeta.toomany")

    if N is not None:
        zeros = zeros_starting_at_N(N, limit)
    else:
        zeros = zeros_starting_at_t(t, limit)

    if fmt == 'plain':
        response = flask.Response(("%d %s\n" % (n, nstr(z,31+floor(log(z,10))+1,strip_zeros=False,min_fixed=-inf,max_fixed=+inf)) for (n, z) in zeros))
        response.headers['content-type'] = 'text/plain'
        if download == "yes":
            response.headers['content-disposition'] = 'attachment; filename=zetazeros'
    else:
        response = str(list(zeros))

    return response
