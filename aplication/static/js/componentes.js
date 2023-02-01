function mensaje_basico(mensaje) {
    Swal.fire(mensaje)
}

function mensaje_con_titulo(titulo_principal, titulo_secundario, icono) {
    Swal.fire(
        titulo_principal,
        titulo_secundario,
        icono
    )
}


function mensaje_success(titulo) {
    Swal.fire({
        position: 'top-end',
        icon: 'success',
        title: titulo,
        showConfirmButton: false,
        timer: 1500
    })
}

function mensaje_error(mensaje, titulo) {
    Swal.fire({
        icon: 'error',
        title: titulo,
        text: mensaje,

    })
}

function mensaje_alerta(mensaje, titulo) {
    Swal.fire({
        icon: 'error',
        title: titulo,
        text: mensaje,

    })
}

function toast_warning(titulo,mensaje) {
    $.toast({
        heading: titulo,
        text: mensaje,
        showHideTransition: 'slide',
        icon: 'warning',
        position: 'top-right',
        stack: false
    })
}

function toast_information(mensaje) {
    $.toast({
        heading: 'Information',
        text: mensaje,
        showHideTransition: 'slide',
        icon: 'info',
        position: 'top-right',
        stack: false
    })
}

function toast_success(mensaje) {
    $.toast({
        heading: 'Success',
        text: mensaje,
        showHideTransition: 'slide',
        icon: 'success',
        position: 'top-right',
        stack: false
    })
}

function toast_simple(mensaje) {
    $.toast(
        {
            text: mensaje,
            position: 'top-right',
            stack: false
        }
    )

}






