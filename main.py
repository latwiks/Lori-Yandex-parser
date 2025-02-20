from flask import Flask, render_template, request, send_file
from excel import excel
from excel_2 import excel_2, excel_to_csv_2, remove_duplicates_csv, remove_duplicates_xlsx
import parser_1
import parser_for_one_image
import time

application = Flask(__name__)


async def isint(x):
    try:
        a = float(x)
        b = int(a)
    except (TypeError, ValueError):
        return False
    else:
        return a == b


@application.route('/', methods=['GET', 'POST'])
async def index():
    error = None
    if request.method == 'POST':
        if not request.form.get('url'):
            error = 'Пожалуйста, заполните поле ввода url.'
        if 'lori.ru' not in request.form.get('url'):
            error = 'Ссылка не на лори'
        if request.form.get('url').startswith('https://'):
            if not await isint(request.form.get('url')[16:]):
                if request.form.get('forma') == 'first':
                    if request.form.get('exorc') == 'excel':
                        try:
                            ids = await parser_1.f(str(request.form.get('url')) + str(request.form.get('sort_by')),
                                                 request.form.get('start_page'),
                                                 request.form.get('end_page'), "db.db")
                            a = await excel("db.db", request.form.get('limiter'), ids[0], ids[1],
                                            str(request.form.get('url'))[16:], request.form.get('sort_by'), False)
                            return send_file(a, as_attachment=True)
                        except Exception as e:
                            error = str(e)
                            print(e)
                            print(e.args)
                            print(str(e))
                            return render_template('index.html', error=error)
                    if request.form.get('exorc') == 'csv':
                        return
                if request.form.get('forma') == 'second':
                    if request.form.get('exorc') == 'excel':
                        if request.form.get('delete') == 'no':
                            try:

                                ids = await parser_1.f(str(request.form.get('url')) + str(request.form.get('sort_by')),
                                                     request.form.get('start_page'),
                                                     request.form.get('end_page'), "db.db")
                                a = await excel_2("db.db", request.form.get('url'), request.form.get('limiter'), ids[0],
                                                  ids[1], request.form.get('sort_by'), False)
                                return send_file(a, as_attachment=True)
                            except Exception as e:
                                error = str(e)
                                print(e)
                                print(e.args)
                                print(str(e))
                                return render_template('index.html', error=error)
                        if request.form.get('delete') == 'yes':
                            start = time.time()
                            ids = await parser_1.f(str(request.form.get('url')) + str(request.form.get('sort_by')),
                                                 request.form.get('start_page'),
                                                 request.form.get('end_page'), "db.db")
                            a = await excel_2("db.db", request.form.get('url'), request.form.get('limiter'), ids[0],
                                              ids[1],
                                              request.form.get('sort_by'), False)
                            b = await remove_duplicates_xlsx("db.db", ids[0], ids[1], str(request.form.get('url'))[16:],
                                                             request.form.get('sort_by'), False)
                            print(time.time() - start)
                            return send_file(b, as_attachment=True)

                    if request.form.get('exorc') == 'csv':
                        if request.form.get('delete') == 'no':
                            try:

                                ids = await parser_1.f(str(request.form.get('url')) + str(request.form.get('sort_by')),
                                                     request.form.get('start_page'),
                                                     request.form.get('end_page'),
                                                     "db.db")
                                a = await excel_to_csv_2("db.db", request.form.get('url'), request.form.get('limiter'),
                                                         ids[0], ids[1], request.form.get('sort_by'), False)
                                return send_file(a, as_attachment=True)
                            except Exception as e:
                                error = str(e)
                                print(e)
                                print(e.args)
                                print(str(e))
                                return render_template('index.html', error=error)
                        if request.form.get('delete') == 'yes':
                            try:
                                ids = await parser_1.f(str(request.form.get('url')) + str(request.form.get('sort_by')),
                                                     request.form.get('start_page'),
                                                     request.form.get('end_page'),
                                                     "db.db")
                                a = await excel_to_csv_2("db.db", request.form.get('url'), request.form.get('limiter'),
                                                         ids[0], ids[1], request.form.get('sort_by'), False)
                                b = await remove_duplicates_csv("db.db", ids[0], ids[1],
                                                                str(request.form.get('url'))[16:],
                                                                request.form.get('sort_by'), False)
                                return send_file(b, as_attachment=True)
                            except Exception as e:
                                error = str(e)
                                print(e)
                                print(e.args)
                                print(str(e))
                                return render_template('index.html', error=error)
            else:
                if request.form.get('forma') == 'first':
                    try:
                        ids = await parser_for_one_image.fetch_image(request.form.get('url'), "db.db")
                        a = await excel("db.db", request.form.get('limiter'), ids[0], ids[1],
                                        str(request.form.get('url'))[16:], '', True)
                        return send_file(a, as_attachment=True)
                    except Exception as e:
                        error = str(e)
                        print(e)
                        print(e.args)
                        print(str(e))
                        return render_template('index.html', error=error)
                if request.form.get('forma') == 'second':
                    if request.form.get('exorc') == 'excel':
                        if request.form.get('delete') == 'no':
                            try:
                                ids = await parser_for_one_image.fetch_image(request.form.get('url'), "db.db")
                                a = await excel_2("db.db", request.form.get('url'), request.form.get('limiter'), ids[0],
                                                  ids[1], '', True)
                                return send_file(a, as_attachment=True)
                            except Exception as e:
                                error = str(e)
                                print(e)
                                print(e.args)
                                print(str(e))
                                return render_template('index.html', error=error)
                        if request.form.get('delete') == 'yes':
                            try:

                                ids = await parser_for_one_image.fetch_image(request.form.get('url'), "db.db")
                                await excel_2("db.db", request.form.get('url'), request.form.get('limiter'), ids[0],
                                              ids[1],
                                              '', True)
                                b = await remove_duplicates_xlsx("db.db", ids[0], ids[1],
                                                                 str(request.form.get('url'))[16:],
                                                                 '', True)
                                return send_file(b, as_attachment=True)
                            except Exception as e:
                                error = str(e)
                                print(e)
                                print(e.args)
                                print(str(e))
                                return render_template('index.html', error=error)
                    if request.form.get('exorc') == 'csv':
                        if request.form.get('delete') == 'no':
                            try:
                                ids = await parser_for_one_image.fetch_image(request.form.get('url'), "db.db")
                                a = await excel_to_csv_2("db.db", request.form.get('url'), request.form.get('limiter'),
                                                         ids[0], ids[1], '', True)
                                return send_file(a, as_attachment=True)
                            except Exception as e:
                                error = str(e)
                                print(e)
                                print(e.args)
                                print(str(e))
                                return render_template('index.html', error=error)
                        if request.form.get('delete') == 'yes':
                            try:
                                ids = await parser_for_one_image.fetch_image(request.form.get('url'), "db.db")
                                await excel_to_csv_2("db.db", request.form.get('url'), request.form.get('limiter'),
                                                     ids[0],
                                                     ids[1], '', True)
                                b = await remove_duplicates_csv("db.db", ids[0], ids[1],
                                                                str(request.form.get('url'))[16:],
                                                                '', True)
                                return send_file(b, as_attachment=True)
                            except Exception as e:
                                error = str(e)
                                print(e)
                                print(e.args)
                                print(str(e))
                                return render_template('index.html', error=error)
        if request.form.get('url').startswith('http://'):
            if not await isint(request.form.get('url')[15:]):
                if request.form.get('forma') == 'first':
                    if request.form.get('exorc') == 'excel':
                        try:
                            ids = await parser_1.f(str(request.form.get('url')) + str(request.form.get('sort_by')),
                                                 request.form.get('start_page'),
                                                 request.form.get('end_page'), "db.db")
                            a = await excel("db.db", request.form.get('limiter'), ids[0], ids[1],
                                            str(request.form.get('url'))[15:], request.form.get('sort_by'), False)
                            return send_file(a, as_attachment=True)
                        except Exception as e:
                            error = str(e)
                            print(e)
                            print(e.args)
                            print(str(e))
                            return render_template('index.html', error=error)
                    if request.form.get('exorc') == 'csv':
                        return
                if request.form.get('forma') == 'second':
                    if request.form.get('exorc') == 'excel':
                        if request.form.get('delete') == 'no':
                            try:
                                ids = await parser_1.f(str(request.form.get('url')) + str(request.form.get('sort_by')),
                                                     request.form.get('start_page'),
                                                     request.form.get('end_page'), "db.db")
                                a = await excel_2("db.db", request.form.get('url'), request.form.get('limiter'), ids[0],
                                                  ids[1], request.form.get('sort_by'), False)
                                return send_file(a, as_attachment=True)
                            except Exception as e:
                                error = str(e)
                                print(e)
                                print(e.args)
                                print(str(e))
                                return render_template('index.html', error=error)
                        if request.form.get('delete') == 'yes':

                            ids = await parser_1.f(str(request.form.get('url')) + str(request.form.get('sort_by')),
                                                 request.form.get('start_page'),
                                                 request.form.get('end_page'), "db.db")
                            a = await excel_2("db.db", request.form.get('url'), request.form.get('limiter'), ids[0],
                                              ids[1],
                                              request.form.get('sort_by'), False)
                            b = await remove_duplicates_xlsx("db.db", ids[0], ids[1], str(request.form.get('url'))[15:],
                                                             request.form.get('sort_by'), False)
                            return send_file(b, as_attachment=True)

                    if request.form.get('exorc') == 'csv':
                        if request.form.get('delete') == 'no':
                            try:

                                ids = await parser_1.f(str(request.form.get('url')) + str(request.form.get('sort_by')),
                                                     request.form.get('start_page'),
                                                     request.form.get('end_page'),
                                                     "db.db")
                                a = await excel_to_csv_2("db.db", request.form.get('url'), request.form.get('limiter'),
                                                         ids[0], ids[1], request.form.get('sort_by'), False)
                                return send_file(a, as_attachment=True)
                            except Exception as e:
                                error = str(e)
                                print(e)
                                print(e.args)
                                print(str(e))
                                return render_template('index.html', error=error)
                        if request.form.get('delete') == 'yes':
                            try:

                                ids = await parser_1.f(str(request.form.get('url')) + str(request.form.get('sort_by')),
                                                     request.form.get('start_page'),
                                                     request.form.get('end_page'),
                                                     "db.db")
                                a = await excel_to_csv_2("db.db", request.form.get('url'), request.form.get('limiter'),
                                                         ids[0], ids[1], request.form.get('sort_by'), False)
                                b = await remove_duplicates_csv("db.db", ids[0], ids[1],
                                                                str(request.form.get('url'))[15:],
                                                                request.form.get('sort_by'), False)
                                return send_file(b, as_attachment=True)
                            except Exception as e:
                                error = str(e)
                                print(e)
                                print(e.args)
                                print(str(e))
                                return render_template('index.html', error=error)
            else:
                if request.form.get('forma') == 'first':
                    try:
                        ids = await parser_for_one_image.fetch_image(request.form.get('url'), "db.db")
                        a = await excel("db.db", request.form.get('limiter'), ids[0], ids[1],
                                        str(request.form.get('url'))[15:], '', True)
                        return send_file(a, as_attachment=True)
                    except Exception as e:
                        error = str(e)
                        print(e)
                        print(e.args)
                        print(str(e))
                        return render_template('index.html', error=error)
                if request.form.get('forma') == 'second':
                    if request.form.get('exorc') == 'excel':
                        if request.form.get('delete') == 'no':
                            try:
                                ids = await parser_for_one_image.fetch_image(request.form.get('url'), "db.db")
                                a = await excel_2("db.db", request.form.get('url'), request.form.get('limiter'), ids[0],
                                                  ids[1], '', True)
                                return send_file(a, as_attachment=True)
                            except Exception as e:
                                error = str(e)
                                print(e)
                                print(e.args)
                                print(str(e))
                                return render_template('index.html', error=error)
                        if request.form.get('delete') == 'yes':
                            try:

                                ids = await parser_for_one_image.fetch_image(request.form.get('url'), "db.db")
                                await excel_2("db.db", request.form.get('url'), request.form.get('limiter'), ids[0],
                                              ids[1],
                                              '', True)
                                b = await remove_duplicates_xlsx("db.db", ids[0], ids[1],
                                                                 str(request.form.get('url'))[15:],
                                                                 '', True)
                                return send_file(b, as_attachment=True)
                            except Exception as e:
                                error = str(e)
                                print(e)
                                print(e.args)
                                print(str(e))
                                return render_template('index.html', error=error)
                    if request.form.get('exorc') == 'csv':
                        if request.form.get('delete') == 'no':
                            try:
                                ids = await parser_for_one_image.fetch_image(request.form.get('url'), "db.db")
                                a = await excel_to_csv_2("db.db", request.form.get('url'), request.form.get('limiter'),
                                                         ids[0], ids[1], '', True)
                                return send_file(a, as_attachment=True)
                            except Exception as e:
                                error = str(e)
                                print(e)
                                print(e.args)
                                print(str(e))
                                return render_template('index.html', error=error)
                        if request.form.get('delete') == 'yes':
                            try:
                                ids = await parser_for_one_image.fetch_image(request.form.get('url'), "db.db")
                                await excel_to_csv_2("db.db", request.form.get('url'), request.form.get('limiter'),
                                                     ids[0],
                                                     ids[1], '', True)
                                b = await remove_duplicates_csv("db.db", ids[0], ids[1],
                                                                str(request.form.get('url'))[15:],
                                                                '', True)
                                return send_file(b, as_attachment=True)
                            except Exception as e:
                                error = str(e)
                                print(e)
                                print(e.args)
                                print(str(e))
                                return render_template('index.html', error=error)

    return render_template('index.html', error=error)


if __name__ == '__main__':
    application.run(debug=True, threaded=True)
