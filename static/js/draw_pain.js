document.addEventListener("DOMContentLoaded", function () {
    const canvas = document.getElementById("painCanvas");
    const drawingInput = document.getElementById("drawing_data");

    if (!canvas || !drawingInput) {
        console.log("Canvas or drawing input not found");
        return;
    }

    const ctx = canvas.getContext("2d");

    let isDrawing = false;
    let lastPosition = null;

    const brushRadius = 32;
    const brushStrength = 0.08;

    function resizeCanvas() {
        const rect = canvas.getBoundingClientRect();

        canvas.width = rect.width;
        canvas.height = rect.height;
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

    function drawAirbrushDot(x, y) {
        const gradient = ctx.createRadialGradient(
            x,
            y,
            0,
            x,
            y,
            brushRadius
        );

        gradient.addColorStop(0, `rgba(220, 53, 69, ${brushStrength})`);
        gradient.addColorStop(0.4, `rgba(220, 53, 69, ${brushStrength * 0.5})`);
        gradient.addColorStop(1, "rgba(220, 53, 69, 0)");

        ctx.fillStyle = gradient;

        ctx.beginPath();
        ctx.arc(x, y, brushRadius, 0, Math.PI * 2);
        ctx.fill();
    }

    function drawBetweenPoints(from, to) {
        const dx = to.x - from.x;
        const dy = to.y - from.y;
        const distance = Math.sqrt(dx * dx + dy * dy);

        const spacing = 4;
        const steps = Math.max(Math.floor(distance / spacing), 1);

        for (let i = 0; i <= steps; i++) {
            const t = i / steps;

            const x = from.x + dx * t;
            const y = from.y + dy * t;

            drawAirbrushDot(x, y);
        }
    }

    function startDrawing(event) {
        event.preventDefault();

        isDrawing = true;

        const position = getPosition(event);
        lastPosition = position;

        drawAirbrushDot(position.x, position.y);
    }

    function draw(event) {
        if (!isDrawing) {
            return;
        }

        event.preventDefault();

        const position = getPosition(event);

        drawBetweenPoints(lastPosition, position);

        lastPosition = position;
    }

    function stopDrawing(event) {
        if (!isDrawing) {
            return;
        }

        event.preventDefault();

        isDrawing = false;
        lastPosition = null;

        drawingInput.value = canvas.toDataURL("image/jpeg", 0.5);
    }

    canvas.addEventListener("mousedown", startDrawing);
    canvas.addEventListener("mousemove", draw);
    canvas.addEventListener("mouseup", stopDrawing);
    canvas.addEventListener("mouseleave", stopDrawing);

    canvas.addEventListener("touchstart", startDrawing, { passive: false });
    canvas.addEventListener("touchmove", draw, { passive: false });
    canvas.addEventListener("touchend", stopDrawing, { passive: false });
});