# AUTO GENERATED FILE - DO NOT EDIT

#' @export
footCustomComponent <- function(id=NULL, data=NULL) {
    
    props <- list(id=id, data=data)
    if (length(props) > 0) {
        props <- props[!vapply(props, is.null, logical(1))]
    }
    component <- list(
        props = props,
        type = 'FootCustomComponent',
        namespace = 'foot_custom_component',
        propNames = c('id', 'data'),
        package = 'footCustomComponent'
        )

    structure(component, class = c('dash_component', 'list'))
}
