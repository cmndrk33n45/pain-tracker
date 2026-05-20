document.addEventListener("DOMContentLoaded", function () {
    const canvas = document.getElementById("painCanvas");
    const drawingInput = document.getElementById("drawing_data");

    if (!canvas || !drawingInput) {
        console.log("Canvas or drawing input not found");
        return;
    }

    const ctx = canvas.getContext("2d");

    let isDrawing = false;

    function resizeCanvas() {
        const rect = canvas.getBoundingClientRect();

        canvas.width = rect.width;
        canvas.height = rect.height;

        ctx.lineWidth = 28;
        ctx.lineCap = "round";
        ctx.lineJoin = "round";
        ctx.strokeStyle = "rgba(220, 53, 69, 0.35)";
    }

    resizeCanvas();
    window.addEventListener("resize", resizeCanvas);

    function getPosition(event) {
        const rect = canvas.getBoundingClientRect();

        let clientX;
        let clientY;

        if (event.touches && event.touches.length > 0) {
            clientX = event.touches[0].clientX;
            clientY = event.touches[0].clientY;
        } else {
            clientX = event.clientX;
            clientY = event.clientY;
        }

        return {
            x: clientX - rect.left,
            y: clientY - rect.top
        };
    }

    function startDrawing(event) {
        event.preventDefault();

        isDrawing = true;

        const position = getPosition(event);

        ctx.beginPath();
        ctx.moveTo(position.x, position.y);
    }

    function draw(event) {
        if (!isDrawing) {
            return;
        }

        event.preventDefault();

        const position = getPosition(event);

        ctx.lineTo(position.x, position.y);
        ctx.stroke();
    }

    function stopDrawing(event) {
        if (!isDrawing) {
            return;
        }

        event.preventDefault();

        isDrawing = false;

        drawingInput.value = canvas.toDataURL("image/png");
    }

    canvas.addEventListener("mousedown", startDrawing);
    canvas.addEventListener("mousemove", draw);
    canvas.addEventListener("mouseup", stopDrawing);
    canvas.addEventListener("mouseleave", stopDrawing);

    canvas.addEventListener("touchstart", startDrawing, { passive: false });
    canvas.addEventListener("touchmove", draw, { passive: false });
    canvas.addEventListener("touchend", stopDrawing, { passive: false });
});