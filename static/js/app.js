document.addEventListener('DOMContentLoaded', function() {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });
});

function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(amount);
}

function calculateNetPay(gross, federal, state, ss, medicare, insurance, retirement, other) {
    const deductions = federal + state + ss + medicare + insurance + retirement + other;
    return gross - deductions;
}

function updatePaycheckPreview() {
    const gross = parseFloat(document.getElementById('gross_pay').value) || 0;
    const federal = parseFloat(document.getElementById('federal_tax').value) || 0;
    const state = parseFloat(document.getElementById('state_tax').value) || 0;
    const ss = parseFloat(document.getElementById('social_security').value) || 0;
    const medicare = parseFloat(document.getElementById('medicare').value) || 0;
    const insurance = parseFloat(document.getElementById('health_insurance').value) || 0;
    const retirement = parseFloat(document.getElementById('retirement_401k').value) || 0;
    const other = parseFloat(document.getElementById('other_deductions').value) || 0;
    
    const net = calculateNetPay(gross, federal, state, ss, medicare, insurance, retirement, other);
    const preview = document.getElementById('net_pay_preview');
    if (preview) {
        preview.textContent = formatCurrency(net);
    }
}

document.querySelectorAll('input[name="gross_pay"], input[name="federal_tax"], input[name="state_tax"], input[name="social_security"], input[name="medicare"], input[name="health_insurance"], input[name="retirement_401k"], input[name="other_deductions"]').forEach(input => {
    input.addEventListener('input', updatePaycheckPreview);
});

function confirmDelete(message) {
    return confirm(message || 'Are you sure you want to delete this item?');
}

const deleteLinks = document.querySelectorAll('a[href*="/delete_"]');
deleteLinks.forEach(link => {
    link.addEventListener('click', function(e) {
        if (!confirmDelete()) {
            e.preventDefault();
        }
    });
});
