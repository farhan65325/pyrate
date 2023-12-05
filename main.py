from flask import Flask, render_template, request
import functions as func
import json

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
    if "submit_form" in request.form:
        if request.form.get("company") and request.form.get("year"):
            company = request.form.get("company")
            year = request.form.get("year")
            risk = None
            indics = json.loads(func.get_indics(company, year, risk))
            quant_indics, quant_sum = func.get_quant_indics(
                company, year, risk)
            qual_indics, qual_sum = func.get_qual_indics(
                company, year, risk)
            nb_points = quant_sum + qual_sum
            final_points = quant_sum * 0.65 + qual_sum * 0.35
            mba_rating = func.get_mba_rating(final_points)
            sp_rating, moodys_rating = func.get_sp_moodys(company, year)
            industry, currency = func.get_currency_and_industry(company)
            return render_template('index.html',
                                   error=None,
                                   indics=indics,
                                   quant_indics=quant_indics,
                                   quant_sum=quant_sum,
                                   qual_indics=qual_indics,
                                   qual_sum=qual_sum,
                                   nb_points=nb_points,
                                   final_points=final_points,
                                   mba_rating=mba_rating,
                                   sp_rating=sp_rating,
                                   moodys_rating=moodys_rating,
                                   company=company.capitalize(),
                                   year=year,
                                   currency=currency,
                                   industry=industry)
        else:
            return render_template('index.html', error="Veuillez vérifier les sélections !")
    return render_template('index.html', error=None)


@app.route('/notation', methods=['GET', 'POST'])
def notation():
    return render_template('notation.html', error=None)


@app.route('/risque', methods=['GET', 'POST'])
def risque():
    return render_template('risque.html', error=None)


@app.route('/agence', methods=['GET', 'POST'])
def agence():
    return render_template('agence.html', error=None)


if __name__ == '__main__':
    app.run(debug=True)
