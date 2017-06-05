$(function () {

    function is_touch_device ()
    {
        try
        {
            document.createEvent("TouchEvent");
            return true;
        } catch (e) {
            return false;
        }
    }

    if (is_touch_device ())    
        $('#nav-mobile').css({ overflow: 'auto'});    

    $('.datagridview').DataTable({ 
        language: { url: '/static/js/spanish.json' },
        "fnInitComplete": function (o) {
            $(".dataTables_length select").addClass("browser-default");
            $(".dataTables_length input[type=search]").focus();
        }
    });    

    $('.button-collapse').sideNav({'edge': 'left'});
    $('select').material_select();
    $('.modal').modal();
    $('.comma-separated').mask("000,000,000,000,000", { reverse: true });

    $('.datepicker').pickadate({
        monthsFull: ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre'],
        selectMonths: true, // Creates a dropdown to control month
        selectYears: 2, // Creates a dropdown of 15 years to control year
        formatSubmit: 'mm-dd-yyyy',
        format: 'Fecha selecciona!da: dd !de mmmm !de yyyy',
        hiddenName: true // para enviar solamente formatSubmit
    });

    $('#form-microbiologia').on('submit', function (e) {
        e.preventDefault();

        $.post('/general/guardar-microbiologia/', $(this).serialize(), function (data) {
            if (data.ok)
            {
                $('#form-microbiologia').trigger('reset');
                Materialize.toast(data.msg, 3000, 'rounded');
                $('#tbody-data').prepend(data.fila);
            }
                
        }, 'json');
    });

    $('#form-conteo-algas').on('submit', function (e) {
        e.preventDefault();

        $.post('/algas/guardar-conteo/', $(this).serialize(), function (data) {
            if (data.ok)
            {
                $('#form-conteo-algas').trigger('reset');
                Materialize.toast(data.msg, 3000, 'rounded');
                $('#datos-algas').prepend(data.fila);
            }
        }, 'json');
    });

    $('#form-filtrar-microbiologia').on('submit', function (e) {
        e.preventDefault();

        var inicio = $("input[name=fecha-inicio]").val();
        var fin = $("input[name=fecha-fin]").val();

        if (inicio != "" && fin != "")
        {
            $.post('/general/filtrar-microbiologia/', $(this).serialize(), function (data) {
                $("#tbody-data").empty();

                data.forEach(function (fila) {
                    $('#tbody-data').append(fila.result);
                });
            });            
        }
    });

    $('.form-nuevo-ciclo').on('submit', function (e) {
        e.preventDefault();

        $('input[name=poblacion_inicial]').unmask();

        $.post('/larvarios/nuevo-ciclo/', $(this).serialize(), function (data) {
            console.log(data.respuesta);
            $('.form-nuevo-ciclo').trigger('reset');
            Materialize.toast(data.respuesta, 3000, 'rounded');

            if (data.hasOwnProperty('sala_id'))
            {
                $sala = $('a#' + data.sala_id);
                $sala.addClass('btn-ciclo-activo');
                $sala.html( $sala.html().replace(/\(.*?\)/, '(' + data.num_ciclo + ')') );
                $('.modal').modal('close');
            }
        }, 'json');
    });

    $('.cerrar-ciclo').click(function (e) {
        e.preventDefault();

        if (!confirm('Confirme cierre de ciclo'))
            return false;

        var sala_id = $(this).attr('data-sala-id');

        $.get('/larvarios/cerrar-ciclo/', {'sala_id': sala_id}, function (data) {
            console.log(data.respuesta);
            Materialize.toast(data.respuesta, 3000, 'rounded');
            $('a#'+sala_id).removeClass('btn-ciclo-activo');
        }, 'json');
    });

    $('#form-datos-maduracion').on('submit', function (e) {
        e.preventDefault();        

        // PENDIENTE DE CAMBIO O ELIMINACION
        // var total_valores = 0;

        // $.each($(this).serialize().split('&'), function (indice, elemento) {
        //     var claves = elemento.split('=');

        //     if (claves[0] != 'csrfmiddlewaretoken')
        //     {
        //         if (claves[0] == '')
        //             total_valores++;
        //     }
                
        // });

        // if (!guardar)
        //     return false;

        $.post('/maduracion/guardar-datos/', $(this).serialize(), function (data) {
            $('#form-datos-maduracion').trigger('reset');
            Materialize.toast(data.respuesta, 3000, 'rounded');
            $('#datos-maduracion').prepend(data.fila);
        }, 'json');
    });

    $('.btn-sala').each(function () {
        var sala_id = $(this).attr('id');
        var $this = $(this);

        $.get('/larvarios/verificar-ciclo-activo/', {'sala_id': sala_id}, function (data) {
            console.log(data.ok + ' ' + data.num_ciclo);

            if (data.ok)
            {
                $this.addClass(data.class);
                $this.html( $this.html() + '(' + data.num_ciclo + ')' );
            } else {
                $this.html( $this.html() + '(' + data.num_ciclo + ')' );
            }

            $('#modal' + sala_id + ' #id_numero_ciclo').val(data.num_ciclo + 1);
        }, 'json');
    });

    $('#form-params-agua').on('submit', function (e) {
        e.preventDefault();

        var source = $(this).attr('data-source');
        var url = (source == 'params-ciclos') ? '/larvarios/' : '/general/';

        $.post(url + 'parametros-agua/guardar/', $(this).serialize(), function (data) {
            $('#form-params-agua').trigger('reset');
            Materialize.toast(data.respuesta, 3000, 'rounded');
            $('#datos-parametros').prepend(data.fila);
        }, 'json');
    });

    $('#form-datos-larva').on('submit', function (e) {
        e.preventDefault();

        var source = $(this).attr('data-source');

        $.post('/larvarios/datos-larva/guardar/', $(this).serialize(), function (data) {
            $('#form-datos-larva').trigger('reset');
            Materialize.toast(data.respuesta, 3000, 'rounded');
            $('#datos-larva').prepend(data.fila);
        }, 'json');
    });

    // function cargar_grafico_parametros (tipo = "line")
    // {
    //     Highcharts.chart('grafico-parametros', {
    //         data:  { table: 'datatable' },
    //         chart: { type:  tipo },
    //         title: { text:  'Parámetros de agua por salas con ciclo activo' },
    //         yAxis: { 
    //             allowDecimals: true,
    //             title: { text: 'Valor según parámetro' }
    //         },
    //         tooltip: { 
    //             formatter: function () {
    //                 return '<strong>' + this.series.name + '</strong><br/>' +
    //                     this.point.y + ' ' + this.point.name.toLowerCase();
    //             }
    //         }
    //     });
    // }


    // cargar_grafico_parametros();

    $('#visualizar-como').on('change', function () {
        cargar_grafico_parametros( $(this).val() );
    });

    var tabla_algas = $("#tabla-algas").tableExport({
        formats: ["xlsx", "csv"],    // (String[]), filetypes for the export
        bootstrap: false,                   // (Boolean), style buttons using bootstrap
        position: "top"
    });

    var tabla_params_general = $("#tabla-params-agua-general").tableExport({
        formats: ["xlsx", "csv"],    // (String[]), filetypes for the export
        bootstrap: false,            // (Boolean), style buttons using bootstrap
        position: "top"
    });

    var tabla_params_larvarios = $("#tabla-params-agua-larvarios").tableExport({
        formats: ["xlsx", "csv"],    // (String[]), filetypes for the export
        bootstrap: false,            // (Boolean), style buttons using bootstrap
        position: "top"
    });


    $('.algas-filtro').on('click', function (e) {
        e.preventDefault();

        $('.algas-filtro').css('text-decoration', 'none');
        $(this).css('text-decoration', 'underline');
        var valor = $(this).attr('data-value');
        var desde = $('.algas-desde').val();
        var hasta = $('.algas-hasta').val();

        $.get('/algas/filtro/', {'filtro': valor, 'desde': desde, 'hasta': hasta}, function (data) {
            console.log(data.respuesta);
            $('#datos-algas').empty().html(data.respuesta);
            tabla_algas.reset()
            cargar_grafico_algas();

        }, 'json');
    });

    $('.params-algas-filtro').on('click', function (e) {
        e.preventDefault();

        $('.params-algas-filtro').css('text-decoration', 'none');
        $(this).css('text-decoration', 'underline');

        var fuente = $('#cbo-fuente-agua').val();
        var fuente_texto = $("#cbo-fuente-agua option:selected" ).text();

        if (fuente == '')
            return;

        var valor = $(this).attr('data-value');

        var GET = {
            'filtro': valor,
            'fuente': fuente,
            'depto': $('#depto').val(),
            'desde': $('.params-algas-desde').val(),
            'hasta': $('.params-algas-hasta').val()
        };

        $.get('/general/filtrar-params-agua/', GET, function (data) {
            console.log(data.respuesta);
            $('#datos-parametros').empty().html(data.respuesta);

            cargar_grafico_params_agua(fuente_texto, 'general');
            tabla_params_general.reset(); // actualiza con los datos de la tabla para generar el excel
        }, 'json');
    });

    $('.params-algas-grafico').on('click', function (e) {
        e.preventDefault();

        $('#grafico-params-agua').toggle();
    });

    $('.params-larva-filtro').on('click', function (e) {
        e.preventDefault();

        $('.params-larva-filtro').css('text-decoration', 'none');
        $(this).css('text-decoration', 'underline');

        var valor = $(this).attr('data-value');
        var idsala = $(this).attr('data-idsala');

        var GET = {
            'filtro': valor,
            'idsala': idsala,
            'desde': $('.params-larva-desde').val(),
            'hasta': $('.params-larva-hasta').val(),
            'script': $('.script').val()
        };

        $.get('/larvarios/filtrar-params-agua/', GET, function (data) {
            console.log(data.respuesta);
            $('#datos-parametros, #datos-larva').empty().html(data.respuesta);

            try
            {
                cargar_grafico_params_agua('Salas', 'larvarios');
                tabla_params_larvarios.reset(); // actualiza con los datos de la tabla para generar el excel                
            } catch (e) {
                console.log(e);
            }
        }, 'json');
    });

    try { cargar_grafico_params_agua('Sala', 'larvarios'); } catch (err) { console.log (err) }
    try { cargar_grafico_algas(); } catch (err) { console.log (err) }


    // --------------------- REPORTES --------------------- //
    var rpt1_tabla = $("#rpt1-tabla").tableExport({
        formats: ["xlsx", "csv"],    // (String[]), filetypes for the export
        bootstrap: false,            // (Boolean), style buttons using bootstrap
        position: "top"
    });
    var rpt2_tabla = $("#rpt2-tabla").tableExport({
        formats: ["xlsx", "csv"],    // (String[]), filetypes for the export
        bootstrap: false,            // (Boolean), style buttons using bootstrap
        position: "top"
    });
    var rpt3_tabla = $("#rpt3-tabla").tableExport({
        formats: ["xlsx", "csv"],    // (String[]), filetypes for the export
        bootstrap: false,            // (Boolean), style buttons using bootstrap
        position: "top"
    });

    $('.rpt1-buscar').on('click', function () {
        var datos_de = $('#rpt1-datosde').val();

        if (datos_de == '') return;

        var desde = $('#rpt1-desde').val();
        var hasta = $('#rpt1-hasta').val();

        $.get('/reporte/rpt1/', {'datos_de': datos_de, 'desde': desde, 'hasta': hasta}, function (data) {
            $('#rpt1-tabla').empty().html(data.respuesta);
            rpt1_tabla.reset();
            rpt_grafico('rpt1');
        }, 'json');

    });

    $('.rpt2-buscar').on('click', function () {
        var datos_de = $('#rpt2-datosde').val();

        if (datos_de == '') return;

        var desde = $('#rpt2-desde').val();
        var hasta = $('#rpt2-hasta').val();

        $.get('/reporte/rpt2/', {'datos_de': datos_de, 'desde': desde, 'hasta': hasta}, function (data) {
            $('#rpt2-tabla').empty().html(data.respuesta);
            rpt2_tabla.reset();
            rpt_grafico('rpt2');
        }, 'json');
    });

    $('.rpt3-buscar').on('click', function () {
        var depto = $('#rpt3-depto').val();
        var muestra = $('#rpt3-muestra').val();
        var desde = $('#rpt3-desde').val();
        var hasta = $('#rpt3-hasta').val();

        if (depto == '') return;
        if (muestra == '') return;

        $.get('/reporte/rpt3/', {'depto': depto, 'muestra': muestra, 'desde': desde, 'hasta': hasta}, function (data) {
            $('#rpt3-tabla').empty().html(data.respuesta);
            rpt3_tabla.reset();
            rpt_grafico('rpt3');
        }, 'json');
    });

    $('.rpt-mostrar-grafico').on('click', function () {
        var rpt = $(this).attr('data-rpt');
        $('#' + rpt + '-grafico').toggle();        
    });



});

function rpt_grafico (rpt, tipo = "line")
{
    var hc = Highcharts.chart(rpt + '-grafico', {
        data:  { table: rpt + '-tabla' },
        chart: { type:  tipo },
        title: { text:  'Conteo de algas' },
        yAxis: { 
            allowDecimals: true,
            title: { text: 'Células/ml' }
        },
        tooltip: { 
            formatter: function () {
                return '<strong>' + this.series.name + '</strong><br/>' +
                    this.point.y + ' ' + this.point.name.toLowerCase();
            }
        },
        plotOptions: {
            line: {
                dataLabels: {
                    enabled: true
                },
                enableMouseTracking: false
            }
        }
    });

    hc.series[4].data[4].graphic.hide();
    hc.series[4].data[4].dataLabel.hide();
}

function cargar_grafico_algas (tipo = "line")
{
    Highcharts.chart('grafico-algas', {
        data:  { table: 'tabla-algas' },
        chart: { type:  tipo },
        title: { text:  'Conteo de algas' },
        yAxis: { 
            allowDecimals: true,
            title: { text: 'Células/ml' }
        },
        tooltip: { 
            formatter: function () {
                return '<strong>' + this.series.name + '</strong><br/>' +
                    this.point.y + ' ' + this.point.name.toLowerCase();
            }
        },
        plotOptions: {
            line: {
                dataLabels: {
                    enabled: true
                },
                enableMouseTracking: false
            }
        }
    });
}

function cargar_grafico_params_agua (fuente, para, tipo = "line")
{
    var div_tabla_id = null;

    if (para == 'general')
        div_tabla_id = 'tabla-params-agua-general';
    else // larvarios
        div_tabla_id = 'tabla-params-agua-larvarios';

    Highcharts.chart('grafico-params-agua', {
        data:  { table: div_tabla_id },
        chart: { type:  tipo },
        title: { text:  'Parámetros de agua en ' + fuente },
        yAxis: { 
            allowDecimals: true,
            title: { text: 'Datos según parámetro' }
        },
        tooltip: { 
            formatter: function () {
                return '<strong>' + this.series.name + '</strong><br/>' +
                    this.point.y + ' ' + this.point.name.toLowerCase();
            }
        },
        plotOptions: {
            line: {
                dataLabels: {
                    enabled: true
                },
                enableMouseTracking: true
            }
        }
    });
}










