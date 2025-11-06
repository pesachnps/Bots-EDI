export default function MetricCard({ title, value, icon: Icon, color, link }) {
  return (
    <div className="overflow-hidden bg-white rounded-lg shadow">
      <div className="p-5">
        <div className="flex items-center">
          <div className={`flex-shrink-0 p-3 rounded-md ${color}`}>
            <Icon className="w-6 h-6 text-white" />
          </div>
          <div className="flex-1 w-0 ml-5">
            <dl>
              <dt className="text-sm font-medium text-gray-500 truncate">{title}</dt>
              <dd className="text-2xl font-semibold text-gray-900">{value}</dd>
            </dl>
          </div>
        </div>
      </div>
      {link && (
        <div className="px-5 py-3 bg-gray-50">
          <a href={link} className="text-sm font-medium text-indigo-600 hover:text-indigo-500">
            View details →
          </a>
        </div>
      )}
    </div>
  );
}
