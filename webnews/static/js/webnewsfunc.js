function theFunc(ElementID,tooltipDiv) {
	//alert(ElementID)

	$(ElementID).tooltipster({
                content: $(tooltipDiv),
				interactive:true
            });

  // code to run when the user hovers over the div
}
