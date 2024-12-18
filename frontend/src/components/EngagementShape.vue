<template>
    <div :class="shapeClass" :style="shapeStyle">
        <span class="ranking" :style="textStyle">{{ artist.rank_data.ranking }}</span>
    </div>
</template>

<script>
export default {
    name: 'EngagementShape',
    props: {
        artist: {
            type: Object,
            required: true
        },
    },
    computed: {
        shapeStyle() {
            // Define a palette of nice-looking base colors for each tier
            const baseColors = {
                0: [255, 223, 99],  // Vibrant Gold for Star
                1: [72, 149, 239],  // Sky Blue for Hexagon
                2: [186, 85, 211],  // Orchid Purple for Pentagon
                3: [60, 179, 113],  // Medium Sea Green for Square
                4: [239, 83, 80]    // Coral Red for Circle
            };

            // Get the base color for the current tier
            const baseColor = baseColors[this.artist.rank_data.tier] || [128, 128, 128]; // Default to gray if tier is undefined

            // Adjust brightness inversely based on percentage
            const brightnessFactor = 1 - this.artist.rank_data.percentage / 100; // Lower percentage = brighter

            // Ensure the last tier retains a hint of its base color
            const minColorFactor = 0.3; // Minimum factor to retain some of the base color
            const adjustedColor = baseColor.map(channel => {
                // Ensure the color stays within a visually appealing range
                const minBrightness = 150; // Minimum brightness to avoid overly dark colors
                const maxBrightness = 255; // Maximum brightness to avoid overly bright colors
                const adjusted = channel * (brightnessFactor * (1 - minColorFactor) + minColorFactor) + minBrightness * (1 - brightnessFactor);
                return Math.min(maxBrightness, Math.max(minBrightness, adjusted));
            });

            // Convert RGB to CSS color string
            const color = `rgb(${adjustedColor.join(',')})`;

            return {
                backgroundColor: color,
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center'
            };
        },
        shapeClass() {
            // Determine the shape based on the tier
            switch (this.artist.rank_data.tier) {
                case 0:
                    return 'star';
                case 1:
                    return 'hexagon';
                case 2:
                    return 'pentagon';
                case 3:
                    return 'square';
                case 4:
                    return 'circle';
                default:
                    return 'square'; // Default shape
            }
        },
        textStyle() {
            // Dynamically adjust text color for readability
            const [r, g, b] = this.shapeStyle.backgroundColor
                .replace(/[^\d,]/g, '') // Extract RGB values
                .split(',')
                .map(Number);

            // Calculate luminance to determine text color
            const luminance = 0.299 * r + 0.587 * g + 0.114 * b;
            return {
                color: luminance > 180 ? 'black' : 'white' // Use black text for bright backgrounds, white for dark
            };
        }
    }
};
</script>

<style scoped>
.circle {
    width: 50px;
    height: 50px;
    border-radius: 50%;
}

.square {
    width: 50px;
    height: 50px;
}

.star {
    height: 80px;
    width: 80px;
    clip-path: polygon(50% 0, 79% 90%, 2% 35%, 98% 35%, 21% 90%);
}

.hexagon {
    width: 60px;
    height: 60px;
    clip-path: polygon(50% 0%, 100% 25%, 100% 75%, 50% 100%, 0% 75%, 0% 25%);
}

.pentagon {
    width: 60px;
    height: 60px;
    clip-path: polygon(50% 0%, 100% 38%, 82% 100%, 18% 100%, 0% 38%);
}

.ranking {
    position: absolute;
    font-size: 20px;
}
</style>