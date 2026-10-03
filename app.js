(() => {
  const terms = {
    spatule: ["Spatule", "L'avant du ski. Sa forme et son relèvement influencent l'entrée en virage, le passage dans la neige souple et le comportement sur les irrégularités."],
    patin: ["Patin", "Partie la plus étroite, mesurée sous la chaussure. La largeur au patin influence notamment la rapidité du changement de carres et la portance en neige profonde."],
    talon: ["Talon", "L'arrière du ski. Son profil, sa rigidité et sa forme modifient notamment la manière dont le ski finit le virage et accompagne le pivot."],
    cotes: ["Lignes de cotes", "Contour latéral du ski : on décrit généralement les largeurs de spatule, de patin et de talon, par exemple 125–82–110 mm. Leur combinaison influence le rayon géométrique et le caractère du ski."],
    rayon: ["Rayon de courbe", "Rayon géométrique théorique issu de la ligne de cotes, exprimé en mètres. Un rayon court favorise en général les courbes serrées et un rayon long les grandes courbes, mais la technique, la déformation et la neige restent déterminantes."],
    fixation: ["Fixations", "Elles relient les chaussures au ski et assurent la transmission des appuis. Les dispositifs de déclenchement visent à réduire certains risques de blessure : choix et réglage doivent être effectués par du personnel qualifié."]
  };
  document.querySelectorAll("[data-term]").forEach(btn => btn.addEventListener("click", () => {
    document.querySelectorAll("[data-term]").forEach(b => b.classList.toggle("is-selected", b===btn));
    const [title, body] = terms[btn.dataset.term];
    document.getElementById("term-heading").textContent = title;
    document.getElementById("term-body").textContent = body;
  }));
  const profiles = {
    classic: ["Cambre classique", "Le milieu du ski est relevé lorsqu'il est posé sans charge. Sous l'appui du skieur, cette courbure se déforme et participe à la répartition de la pression, à l'accroche et à la relance.", "M70 128 Q110 214 188 214 C300 214 352 188 490 188 C628 188 680 214 792 214 Q870 214 910 152"],
    tip: ["Rocker avant", "La spatule commence à se relever plus tôt. La longueur de contact au sol peut diminuer en position neutre, ce qui facilite souvent l'entrée en virage et aide en neige souple.", "M70 105 Q130 198 255 214 C330 214 380 187 490 188 C610 188 682 214 792 214 Q865 214 910 152"],
    double: ["Double rocker", "La spatule et le talon se relèvent plus tôt. Le ski est souvent plus facile à faire pivoter, notamment en neige souple ; sa tenue sur neige dure dépend également du cambre, de la construction et du flex.", "M70 105 Q132 195 244 214 C330 214 382 188 490 188 C598 188 650 214 745 214 Q855 195 910 105"],
    low: ["Faible cambre", "Le ski possède une arche moins marquée sous le pied, souvent associée à une sensation plus accessible et progressive. Son comportement dépend fortement de la rigidité et des rockers éventuels.", "M70 128 Q110 214 188 214 C308 214 370 202 490 202 C610 202 672 214 792 214 Q870 214 910 152"],
    full: ["Full rocker", "Le ski est courbé à l'inverse d'un cambre traditionnel, avec les extrémités relevées et la zone centrale plus proche de la neige. Le pivot et le comportement en neige profonde sont favorisés, au détriment généralement de la conduite sur neige dure.", "M70 97 C190 167 350 211 490 214 C630 211 790 167 910 97"]
  };
  document.querySelectorAll("[data-profile]").forEach(btn => btn.addEventListener("click", () => {
    document.querySelectorAll("[data-profile]").forEach(b => b.classList.toggle("is-selected", b===btn));
    const [title, body, path] = profiles[btn.dataset.profile];
    document.getElementById("profile-title").textContent = title;
    document.getElementById("profile-text").textContent = body;
    document.getElementById("profile-line").setAttribute("d", path);
    document.getElementById("profile-highlight").setAttribute("d", path);
  }));
})();