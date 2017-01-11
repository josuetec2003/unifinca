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
                $('a#'+data.sala_id).addClass('btn-ciclo-activo');
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

        $.post('/maduracion/guardar-datos-maduracion/', $(this).serialize(), function (data) {
            $('#form-datos-maduracion').trigger('reset');
            Materialize.toast(data.respuesta, 3000, 'rounded');
            $('#datos-maduracion').prepend(data.fila);
        }, 'json');
    });

    $('.btn-sala').each(function () {
        var sala_id = $(this).attr('id');
        var $this = $(this);
        $.get('/larvarios/verificar-ciclo-activo/', {'sala_id': sala_id}, function (data) {
            if (data.ok)
                $this.addClass(data.class);
        }, 'json');
    });

    $('#form-guardar-params').on('submit', function (e) {
        e.preventDefault();

        $.post('/larvarios/parametros-agua/guardar/', $(this).serialize(), function (data) {
            $('#form-guardar-params').trigger('reset');
            Materialize.toast(data.respuesta, 3000, 'rounded');
            $('#datos-parametros').prepend(data.fila);
        }, 'json');
    });

    function cargar_grafico_parametros (tipo = "column")
    {
        Highcharts.chart('grafico-parametros', {
            data:  { table: 'datatable' },
            chart: { type:  tipo },
            title: { text:  'Parámetros de agua por salas con ciclo activo' },
            yAxis: { 
                allowDecimals: true,
                title: { text: 'Valor según parámetro' }
            },
            tooltip: {
                formatter: function () {
                    return '<strong>' + this.series.name + '</strong><br/>' +
                        this.point.y + ' ' + this.point.name.toLowerCase();
                }
            }
        });
    }

    cargar_grafico_parametros();

    $('#visualizar-como').on('change', function () {
        cargar_grafico_parametros($(this).val());
    }); 

})


