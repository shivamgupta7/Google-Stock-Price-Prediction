var chartPredictedData;
// <!--       var chartActualData; -->

        function requestData()
        {
            // Ajax call to get the Data from Flask
            var requests = $.get('/data');

            var tm = requests.done(function (result)
            {
                // predicted
                var seriesPredictedData = chartPredictedData.series[0],
                    shiftPredictedData = seriesPredictedData.data.length > 20;

                // Actual Data
                var seriesActualData = chartPredictedData.series[1],
                    shiftActualData = seriesPredictedData.data.length > 20;

                // Add the Point
                // Time PredictedData\
                var data1 = [];

                data1.push(result[0]);
                data1.push(result[1]);


                // Add the Point
                // Time Actual Data
                var data2 = [];
                data2.push(result[0]);
                data2.push(result[2]);


                chartPredictedData.series[0].addPoint(data1, true, shiftPredictedData);
                chartPredictedData.series[1].addPoint(data2, true, shiftActualData);

                $(".sensor1").text("");
                $(".sensor1").text("Predicted : " +  data1[1] );

                $(".sensor2").text("");
                $(".sensor2").text("Actual : " +  data2[1] );

                // call it again after one secmnmond
                setTimeout(requestData, 2000);

            });
        }

        $(document).ready(function()
        {
            // --------------Chart  ----------------------------
            chartPredictedData = Highcharts.stockChart({

                chart:
                    {
                    renderTo: 'data-PredictedData',
                    defaultSeriesType: 'spline',
                    zoomType: 'xy',

                    events: {
                        load: requestData
                            }
                    },
                title:
                    {
                    text: 'Google Stock Price'
                    },
                rangeSelector: {
                    selected: 4
                },
                xAxis: {
                    type: 'datetime',
                    labels:{
                        format: '{value:%e-%m-%y %H:%M:%S}'
                            },
                    tickPixelInterval: 150,
                    maxZoom: 20 * 1000
                        },
                yAxis: {
                    lineWidth: 1,
                    minPadding: 0.2,
                    maxPadding: 0.2,
                    title: {
                        text: 'Value',
                        margin: 20
                            }

                         },


                series: [{
                    color : '#c23d23',
                    lineColor: '#303030',
                    name: 'Predicted Price',
                    data: [] },
                    {
                    lineColor: '#1d82b8',
                    name: 'Actual Price',
                    data: []
                }],

            });

        });
        $('#button').click(function () {
            chart.xAxis[0].setExtremes(
                Date.UTC(2020, 1, 1),
                Date.UTC(2020, 11, 31)
    );
});