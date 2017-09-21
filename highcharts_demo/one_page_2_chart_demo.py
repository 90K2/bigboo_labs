from highcharts import Highchart
import os


def main():
    chart_number = 2

    base_dir = os.path.dirname(os.path.realpath(__file__))
    filename = os.path.join(base_dir, 'page.html')
    try:
        os.remove(filename)
    except OSError:
        pass

    main_chart = Highchart()
    main_chart.buildhtml()

    with open(filename, mode='w') as f:
        f.write(main_chart.htmlheader)
        for i in range(chart_number):

            chart = Highchart()
            chart_options = {
                'chart': {
                    'renderTo': 'container%s' % i
                },
                'title': {
                    'text': 'Chart number %s' % i
                },
                'subtitle': {
                    'text': 'Chart description'
                },
                'xAxis': {
                    'categories': [1, 2, 3, 4, 5]
                },
                'yAxis': {
                    'allowDecimals': False,
                    'min': 0,
                    'title': {
                        'text': 'Time (min)'
                    }
                },
                'tooltip': {
                    'formatter': "function () {\
                                    return '<b>' + this.x + '</b><br/>' +\
                                        this.series.name + ': ' + this.y + '<br/>' +\
                                        'Total: ' + this.point.stackTotal;\
                                }"
                },
                'plotOptions': {
                    'column': {
                        'stacking': 'normal'
                    }
                }
            }
            chart.set_dict_options(chart_options)

            chart.add_data_set([1, 2, 3, 4, 5], 'column', 'name', stack='by_step', color='#5deae8')

            chart.buildcontainer()
            chart.buildcontent()
            f.write(chart._htmlcontent.decode())

    f.close()


if __name__ == '__main__':
    main()
