function loadFlip(userAuth, userPersonaname, id, cPersonaname, cAvatarLink, cSkins, creatorChoseRed, jPersonaname = "None", jAvatarLink = "None", jSkins = "None") {

    player1_skins_card = React.createElement("div", {className: "card w-100 h-100"},
        React.createElement("div", {className: "card-body m-0 p-0 h-100 w-100"}))
    player2_skins_card = React.createElement("div", {className: "card w-100 h-100"},
        React.createElement("div", {className: "card-body m-0 p-0 h-100 w-100"}))

    var player1_value = 0.00
    var player2_value = 0.00

    creatorSkins = JSON.parse(cSkins);
    joinerSkins = JSON.parse(jSkins);


    player1_nameval_col = React.createElement("div", {className: "col-lg-9 col-md-12 p-0 m-0"},
        player1_name_row = React.createElement("div", {className: "row w-100 h-50 p-0 pt-4 ps-2 m-0 align-items-center", style: {overflow: "hidden"}},
           React.createElement("h5", {className: "w-100 mw-100 p-0 m-0 text-nowrap overflow-hidden", style: {textOverflow: "ellipsis"}}, cPersonaname) ),
        player1_value_row = React.createElement("div", {className: "row w-100 h-50 p-0 pb-4 ps-2 m-0 align-items-center"},
           React.createElement("h5", {className: "w-100 mw-100 p-0 m-0 text-nowrap overflow-hidden", style: {wordWrap: "none"}}, ("$" + player1_value))))

    player1_image_col = React.createElement("div", {className: "col-3 d-lg-flex d-md-none d-sm-none m-0 p-0 ps-2 align-items-center"},
        React.createElement("img", {className: "w-100 h-auto", src: cAvatarLink, style: {borderRadius: "0.375rem 0.375rem 0.375rem 0.375rem"}}))

    player2_nameval_col = React.createElement("div", {className: "col-lg-9 col-md-12 p-0 m-0"},
        player2_name_row = React.createElement("div", {className: "row w-100 h-50 p-0 pt-4 ps-2 m-0 align-items-center", style: {overflow: "hidden"}},
           React.createElement("h5", {className: "w-100 mw-100 p-0 m-0 text-nowrap overflow-hidden", style: {textOverflow: "ellipsis"}}, jPersonaname) ),
        player2_value_row = React.createElement("div", {className: "row w-100 h-50 p-0 pb-4 ps-2 m-0 align-items-center"},
           React.createElement("h5", {className: "w-100 mw-100 p-0 m-0 text-nowrap overflow-hidden", style: {wordWrap: "none"}}, ("$" + player2_value))))


    player2_image_col = React.createElement("div", {className: "col-3 d-lg-flex d-md-none d-sm-none m-0 p-0 ps-2 align-items-center"},
        React.createElement("img", {className: "w-100 h-auto", src: jAvatarLink, style: {borderRadius: "0.375rem 0.375rem 0.375rem 0.375rem"}}))


    join_button = React.createElement("button", {className: "btn btn-success m-0 p-0 h-100 w-100 flipbutton", id : "joinbutton"}, "Join")
    view_button = React.createElement("button", {className: "btn btn-secondary m-0 p-0 h-100 w-100 flipbutton", id: "viewbutton"}, "View")

    if(userAuth == 'True' && userPersonaname != String(cPersonaname) && (jPersonaname == "")){ 
        join_row = React.createElement("div", {className: "row w-100 h-50 p-2 m-0 justify-content-center", }, join_button)
    }
    else {
        join_row = React.createElement("div", {style: {display: 'none'}})
    }
    view_row = React.createElement("div", {className: "row w-100 h-50 p-2 m-0 justify-content-center"}, view_button)

    player1_skins_col = React.createElement("div", {className: "col-6 h-100 p-2 m-0"}, player1_skins_card)

    if(jPersonaname != ""){
    player2_skins_col = React.createElement("div", {className: "col-6 h-100 p-2 m-0"}, player2_skins_card)
    }
    else{
        player2_skins_col = React.createElement("div", {className: "d-none"})
    }

    player1_info_col = React.createElement("div", {className: "col-6 h-100 p-0 m-0 pl-2", style: {borderRadius: "0.375rem 0 0 0.375rem"}},
        player1_info_row = React.createElement("div", {className: "row w-100 h-100 p-0 m-0"}, player1_image_col, player1_nameval_col))
    
    if(jPersonaname != ""){
    player2_info_col = React.createElement("div", {className: "col-6 h-100 p-0 m-0 pl-2", style: {borderRadius: "0.375rem 0 0 0.375rem"}},
        player2_info_row = React.createElement("div", {className: "row w-100 h-100 p-0 m-0"}, player2_image_col, player2_nameval_col))
    }
    else{
        player2_info_col = React.createElement("div", {className: "d-none"})
    }

    flip_content = React.createElement("div", {className: "card-body p-0 h-100 flipcardbody", style: {border: "none"}},
        React.createElement("div", {className: "row w-100 h-100 p-0 m-0 align-items-center justify-content-around"},
            React.createElement("div", {className: "col h-100 p-0 m-0 d-inline-block align-middle"},
                player1_row = React.createElement("div", {className: "row w-100 h-100 p-0 m-0 align-items-center"}, player1_info_col, player1_skins_col)),
            
            buttons_col = React.createElement("div", {className: "col-1 h-100 p-0 m-0 border border-top-0 border-bottom-0",}, join_row, view_row),
            
            React.createElement("div", {className: "col h-100 p-0 m-0 d-inline-block align-middle"},
                player2_row = React.createElement("div", {className: "row w-100 h-100 p-0 m-0 align-items-center"}, player2_info_col, player2_skins_col))
        )
    )

    ReactDOM.render(flip_content, document.getElementById('flip-' + id))
}