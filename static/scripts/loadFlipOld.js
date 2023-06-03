function loadFlipOld(id, creatorId, creatorPersonaname, creatorAvatar, creatorStatus, creatorChoseRed, creatorSkins, joinerId = "None", joinerPersonaname = "None", joinerAvatar = "None", joinerStatus = "None", joinerSkins = "None"){

    // Card
    card = document.createElement("div");
    card.className = "card p-0 m-0 mt-1 mb-1 w-100 flipcard"
    card.dataset.bsTheme = "dark";
    cardBody = document.createElement("div");
    cardBody.className = "card-body p-0 h-100 flipcardbody";

    // Parent row
    parentRow = document.createElement("div");
    parentRow.className = "row w-100 h-100 p-0 m-0 align-items-center justify-content-around";

    // Player 1 col-5
    player1col = document.createElement("div");
    player1col.className = "col h-100 p-0 d-inline-block align-middle";

    // Player 1 row
    player1info = document.createElement("div");
    player1info.className = "row w-100 h-100 p-0 m-0 align-items-center";
    player1info.style.borderRadius = "0.375rem 0 0 0.375rem";

    // Player 1 image column
    player1imagecol = document.createElement("div");
    player1imagecol.className = "col-1 d-none d-lg-block p-0 ms-3";
    player1imagecol.style.position = "relative";
    player1img = document.createElement("img");
    player1img.className = "rounded-circle shadow-4-strong playerimg";
    player1img.src = creatorAvatar;
    player1img.style.border = "solid medium";
    
    if(String(creatorChoseRed).toLowerCase() == 'true'){
      player1info.style.background = "linear-gradient(90deg, rgba(255,0,0,0.75) 0%, rgba(0,212,255,0) 60%)";
      player1img.style.borderColor = 'red';
    } 
    else{
      player1info.style.background = "linear-gradient(90deg, rgba(0,0,0,0.9) 0%, rgba(0,212,255,0) 60%)";
      player1img.style.borderColor = 'black';
    }

    // Player 1 namevalue column
    player1namevaluecol = document.createElement("div");
    player1namevaluecol.className = "col-5 p-0 ps-2 m-0";

    // Player 1 skins column
    player1skins = document.createElement("div");
    player1skins.className = "col h-100 align-self-end m-0 p-0";
    player1skinscard = document.createElement("div");
    player1skinscard.className = "card m-2 p-1 w-95 h-6rem skinscard";
    player1skinsbody = document.createElement("div");
    player1skinsbody.className = "card-body m-0 p-0 h-100 w-100";

    player1skinsrow = document.createElement("div");
    player1skinsrow.className = "row m-0 p-0 h-100 w-100 jutsify-content-around align-items-center";

    let player1floatvalue = 0.00;

    creatorSkins = JSON.parse(creatorSkins);

    for (let i = 0; i < creatorSkins.length; i++) {

      skincol = document.createElement("div");
      skincol.className = "col-3";

      skinimage = document.createElement("img");
      skinimage.className = "skinimage m-0 p-0";
      skinimage.src = "https://community.cloudflare.steamstatic.com/economy/image/" + creatorSkins[i]['image_url']
      skincol.appendChild(skinimage);
      player1skinsrow.appendChild(skincol)
      player1floatvalue += parseFloat(creatorSkins[i]['price'])
    }
    
    player1skinsbody.appendChild(player1skinsrow);
    player1skinscard.appendChild(player1skinsbody);

    // Player 1 name row
    player1namerow = document.createElement("div");
    player1namerow.className = "row w-100 h-50 p-0 m-0 align-items-center";
    player1namecol = document.createElement("div");
    player1namecol.className = "col-12 p-0 m-0";
    player1name = document.createElement("h5");
    player1name.className = "player1name text-nowrap overflow-hidden playerinfotext";
    player1name.innerHTML = creatorPersonaname + "  ";

    // Player 1 value row
    player1valuerow = document.createElement("div");
    player1valuerow.className = "row w-100 h-50 p-0 m-0 align-items-center";
    player1valuecol = document.createElement("div");
    player1valuecol.className = "col-12 p-0 m-0";
    player1value = document.createElement("h5");
    player1value.className = "playerinfotext";
    italics = document.createElement("i");
    italics.innerHTML = "$" + Math.round(player1floatvalue * 100) / 100;
    italics.className = "text-nowrap overflow-hidden"
    player1value.appendChild(italics)
    player1value.style.color = "#F5F5F5";

    // Player 2 col-5
    player2col = document.createElement("div");
    player2col.className = "col h-100 p-0 d-inline-block align-middle";

    // Player 2 row
    player2info = document.createElement("div");
    player2info.className = "row w-100 h-100 p-0 m-0 align-items-center";
    player2info.style.borderRadius = "0 0.375rem 0.375rem 0";

    // Player 2 image column
    player2imagecol = document.createElement("div");
    player2imagecol.className = "col-1 d-none d-lg-block p-0 me-3";
    player2imagecol.style.position = "relative";
    player2img = document.createElement("img");
    player2img.className = "rounded-circle shadow-4-strong playerimg";
    player2img.style.position = "relative";
    player2img.src = joinerAvatar;
    player2img.style.border = "solid medium";

    if(String(creatorChoseRed).toLowerCase() == 'true'){
     player2img.style.borderColor = 'black';
     player2info.style.background = "linear-gradient(270deg, rgba(0,0,0,0.9) 0%, rgba(0,212,255,0) 60%)";
    } 
    else{
      player2info.style.background = "linear-gradient(270deg, rgba(255,0,0,0.75) 0%, rgba(0,212,255,0) 60%)";
      player2img.style.borderColor = 'red';
    }

    // Player 2 namevalue column
    player2namevaluecol = document.createElement("div");
    player2namevaluecol.className = "col-5 p-0 pe-2 m-0";

    // Player 2 skins column
    player2skins = document.createElement("div");
    player2skins.className = "col h-100 align-self-start m-0 p-0";
    player2skinscard = document.createElement("div");
    player2skinscard.className = "card m-2 p-0 w-95 skinscard";
    
    // Player 2 name row
    player2namerow = document.createElement("div");
    player2namerow.className = "row w-100 h-50 p-0 m-0";
    player2namecol = document.createElement("div");
    player2namecol.className = "col-12 p-0 m-0 player2textparent player2name";
    player2name = document.createElement("h5");
    player2name.className = "text-nowrap overflow-hidden playerinfotext";
    player2name.innerHTML = joinerPersonaname + "  ";

    // Player 2 value row
    player2valuerow = document.createElement("div");
    player2valuerow.className = "row w-100 h-50 p-0 m-0";
    player2valuecol = document.createElement("div");
    player2valuecol.className = "col-12 p-0 m-0";
    player2value = document.createElement("h5");
    player2value.className = "playerinfotext text-right player2textparent";
    italics = document.createElement("i");
    italics = document.createElement("i");
    italics.innerHTML = "$9.99";
    player2value.appendChild(italics)
    player2value.style.color = "#F5F5F5";
  
    // Buttons
    buttonscol = document.createElement("div");
    buttonscol.className = "col-1 h-100 align-self-end m-0 p-1";
    joinrow = document.createElement("div");
    joinrow.className = "row w-100 h-50 p-0 m-0 justify-content-end";
    viewrow = document.createElement("div");
    viewrow.className = "row w-100 h-50 p-0 m-0 justify-content-end";
    joincol = document.createElement("div");
    joincol.className = "col-12 m-0 p-1 h-100";
    viewcol = document.createElement("div");
    viewcol.className = "col-12 m-0 p-1 h-100";
    joinbutton = document.createElement("button");
    joinbutton.className = "btn btn-success m-0 p-0 h-100 w-100 flipbutton";
    joinbutton.id = 'joinbutton';
    joinbutton.setAttribute('data', id);

    joinbutton.innerHTML = "Join";
    viewbutton = document.createElement("button");
    viewbutton.id = "viewbutton";
    viewbutton.setAttribute('data', id);
    viewbutton.className = "btn btn-secondary m-0 p-0 w-100 h-100 flipbutton";
    viewbutton.innerHTML = "View";

    if(String('{{ current_user.is_authenticated }}') == 'True' && String(('{{ current_user.id }}')) != String(creatorId) && (joinerId == "None" || joinerId == "")){  
        joincol.appendChild(joinbutton);
    }
    
    player1namecol.appendChild(player1name);
    player1valuecol.appendChild(player1value);

    player1namerow.appendChild(player1namecol);
    player1valuerow.appendChild(player1valuecol);

    player1namevaluecol.appendChild(player1namerow);
    player1namevaluecol.appendChild(player1valuerow);

    player2namecol.appendChild(player2name);
    player2valuecol.appendChild(player2value);

    player2namerow.appendChild(player2namecol);
    player2valuerow.appendChild(player2valuecol);

    player2namevaluecol.appendChild(player2namerow);
    player2namevaluecol.appendChild(player2valuerow);

    viewcol.appendChild(viewbutton);
    joinrow.appendChild(joincol);
    viewrow.appendChild(viewcol);
    buttonscol.appendChild(joinrow);
    buttonscol.appendChild(viewrow);
    
    player1skins.appendChild(player1skinscard);
    player2skins.appendChild(player2skinscard)
    player1imagecol.appendChild(player1img);
    player2imagecol.appendChild(player2img);
    player1info.appendChild(player1imagecol);
    player1info.appendChild(player1namevaluecol);
    player1info.appendChild(player1skins);
    player1col.appendChild(player1info);

    if(joinerId != "None" && joinerId != ""){

    player2info.appendChild(player2skins);
    player2info.appendChild(player2namevaluecol);
    player2info.appendChild(player2imagecol);
    }
    player2col.appendChild(player2info);

    // Parent Appending
    parentRow.appendChild(player1col);
    parentRow.appendChild(buttonscol);
    parentRow.appendChild(player2col);
    cardBody.appendChild(parentRow);
    card.appendChild(cardBody);

    var target = document.getElementById('flip-'+id)
    target.innerHTML = card.innerHTML;
}