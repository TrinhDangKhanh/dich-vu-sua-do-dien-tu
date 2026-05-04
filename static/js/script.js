// Custom JavaScript for PC Care System

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Auto-hide alerts after 5 seconds
    setTimeout(function() {
        var alerts = document.querySelectorAll('.alert');
        alerts.forEach(function(alert) {
            var bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);

    // Form validation
    var forms = document.querySelectorAll('.needs-validation');
    forms.forEach(function(form) {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });

    // Confirm delete actions
    var deleteButtons = document.querySelectorAll('[data-confirm-delete]');
    deleteButtons.forEach(function(button) {
        button.addEventListener('click', function(event) {
            var message = this.getAttribute('data-confirm-delete') || 'Bạn có chắc chắn muốn xóa?';
            if (!confirm(message)) {
                event.preventDefault();
            }
        });
    });

    // Phone number formatting
    var phoneInputs = document.querySelectorAll('input[type="tel"]');
    phoneInputs.forEach(function(input) {
        input.addEventListener('input', function(e) {
            var value = e.target.value.replace(/\D/g, '');
            if (value.length > 0) {
                if (value.length <= 4) {
                    e.target.value = value;
                } else if (value.length <= 7) {
                    e.target.value = value.slice(0, 4) + ' ' + value.slice(4);
                } else {
                    e.target.value = value.slice(0, 4) + ' ' + value.slice(4, 7) + ' ' + value.slice(7, 11);
                }
            }
        });
    });

    // Currency formatting
    var currencyInputs = document.querySelectorAll('input[type="number"][data-currency]');
    currencyInputs.forEach(function(input) {
        input.addEventListener('blur', function(e) {
            var value = parseFloat(e.target.value);
            if (!isNaN(value)) {
                e.target.value = value.toLocaleString('vi-VN');
            }
        });

        input.addEventListener('focus', function(e) {
            var value = e.target.value.replace(/\./g, '');
            e.target.value = value;
        });
    });

    // Search functionality
    var searchInputs = document.querySelectorAll('[data-search]');
    searchInputs.forEach(function(input) {
        var searchTimeout;
        input.addEventListener('input', function(e) {
            clearTimeout(searchTimeout);
            var searchTerm = e.target.value.toLowerCase();
            var targetSelector = e.target.getAttribute('data-search');
            var targets = document.querySelectorAll(targetSelector);

            searchTimeout = setTimeout(function() {
                targets.forEach(function(target) {
                    var text = target.textContent.toLowerCase();
                    var row = target.closest('tr');
                    if (text.includes(searchTerm)) {
                        row.style.display = '';
                    } else {
                        row.style.display = 'none';
                    }
                });
            }, 300);
        });
    });

    // Table sorting
    var sortableTables = document.querySelectorAll('.table-sortable');
    sortableTables.forEach(function(table) {
        var headers = table.querySelectorAll('th[data-sort]');
        headers.forEach(function(header) {
            header.style.cursor = 'pointer';
            header.addEventListener('click', function() {
                var column = this.getAttribute('data-sort');
                var tbody = table.querySelector('tbody');
                var rows = Array.from(tbody.querySelectorAll('tr'));
                var isAscending = this.classList.contains('sort-asc');

                // Remove existing sort classes
                headers.forEach(function(h) {
                    h.classList.remove('sort-asc', 'sort-desc');
                });

                // Sort rows
                rows.sort(function(a, b) {
                    var aValue = a.querySelector('[data-sort-column="' + column + '"]').textContent;
                    var bValue = b.querySelector('[data-sort-column="' + column + '"]').textContent;

                    if (isAscending) {
                        return aValue.localeCompare(bValue);
                    } else {
                        return bValue.localeCompare(aValue);
                    }
                });

                // Toggle sort direction
                this.classList.toggle('sort-asc');
                this.classList.toggle('sort-desc');

                // Reorder rows
                rows.forEach(function(row) {
                    tbody.appendChild(row);
                });
            });
        });
    });

    // Print functionality
    var printButtons = document.querySelectorAll('[data-print]');
    printButtons.forEach(function(button) {
        button.addEventListener('click', function() {
            var printTarget = this.getAttribute('data-print');
            if (printTarget) {
                var element = document.querySelector(printTarget);
                if (element) {
                    var printWindow = window.open('', '_blank');
                    printWindow.document.write('<html><head><title>Print</title>');
                    printWindow.document.write('<style>body{font-family:Arial,sans-serif;padding:20px;}');
                    printWindow.document.write('table{width:100%;border-collapse:collapse;}');
                    printWindow.document.write('th,td{border:1px solid #ddd;padding:8px;text-align:left;}');
                    printWindow.document.write('th{background-color:#f2f2f2;}');
                    printWindow.document.write('</style></head><body>');
                    printWindow.document.write(element.innerHTML);
                    printWindow.document.write('</body></html>');
                    printWindow.document.close();
                    printWindow.print();
                }
            } else {
                window.print();
            }
        });
    });

    // Export to CSV
    var exportButtons = document.querySelectorAll('[data-export-csv]');
    exportButtons.forEach(function(button) {
        button.addEventListener('click', function() {
            var tableSelector = this.getAttribute('data-export-csv');
            var table = document.querySelector(tableSelector);
            if (table) {
                var csv = [];
                var rows = table.querySelectorAll('tr');
                
                rows.forEach(function(row) {
                    var cols = row.querySelectorAll('th, td');
                    var rowData = [];
                    cols.forEach(function(col) {
                        var text = col.textContent.trim();
                        // Escape quotes and wrap in quotes if contains comma
                        if (text.includes(',') || text.includes('"')) {
                            text = '"' + text.replace(/"/g, '""') + '"';
                        }
                        rowData.push(text);
                    });
                    csv.push(rowData.join(','));
                });

                var csvContent = csv.join('\n');
                var blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
                var link = document.createElement('a');
                var url = URL.createObjectURL(blob);
                
                link.setAttribute('href', url);
                link.setAttribute('download', 'export_' + new Date().toISOString().slice(0, 10) + '.csv');
                link.style.visibility = 'hidden';
                
                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);
            }
        });
    });

    // Loading states
    var loadingButtons = document.querySelectorAll('[data-loading]');
    loadingButtons.forEach(function(button) {
        button.addEventListener('click', function() {
            var originalText = this.innerHTML;
            this.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Đang xử lý...';
            this.disabled = true;

            // Reset after 3 seconds (for demo purposes)
            setTimeout(function() {
                button.innerHTML = originalText;
                button.disabled = false;
            }, 3000);
        });
    });

    // Auto-refresh functionality
    var autoRefreshElements = document.querySelectorAll('[data-auto-refresh]');
    autoRefreshElements.forEach(function(element) {
        var interval = parseInt(element.getAttribute('data-auto-refresh')) || 30000;
        setInterval(function() {
            // Trigger refresh
            var event = new CustomEvent('autoRefresh');
            element.dispatchEvent(event);
        }, interval);
    });
});

// Utility functions
function formatCurrency(amount) {
    return new Intl.NumberFormat('vi-VN', {
        style: 'currency',
        currency: 'VND'
    }).format(amount);
}

function formatDate(date) {
    return new Intl.DateTimeFormat('vi-VN', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit'
    }).format(date);
}

function showAlert(message, type = 'info') {
    var alertContainer = document.getElementById('alert-container') || document.body;
    var alertElement = document.createElement('div');
    alertElement.className = 'alert alert-' + type + ' alert-dismissible fade show';
    alertElement.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    alertContainer.appendChild(alertElement);
    
    // Auto-remove after 5 seconds
    setTimeout(function() {
        if (alertElement.parentNode) {
            alertElement.parentNode.removeChild(alertElement);
        }
    }, 5000);
}

function confirmAction(message, callback) {
    if (confirm(message)) {
        callback();
    }
}

// Global error handler
window.addEventListener('error', function(e) {
    console.error('JavaScript error:', e.error);
    showAlert('Đã xảy ra lỗi không mong muốn. Vui lòng thử lại.', 'danger');
});

// AJAX helper
function ajaxRequest(url, options = {}) {
    var defaultOptions = {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest'
        }
    };

    options = Object.assign(defaultOptions, options);

    return fetch(url, options)
        .then(function(response) {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .catch(function(error) {
            console.error('AJAX error:', error);
            showAlert('Không thể kết nối đến máy chủ. Vui lòng thử lại.', 'danger');
            throw error;
        });
}
